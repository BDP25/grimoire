import json
from pathlib import Path
from typing import cast

from langchain_postgres import PGVector
from meta import EvalAnswer, EvalQuestion
from questions import questions
from tqdm import tqdm

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    ProjectConfiguration,
)
from grimoire.helpers.llm import setup_llm
from grimoire.helpers.retriever import get_retrieval_chain
from grimoire.helpers.vectorstore import setup_vectorstore, vectorstore_connection


def ask(config: ProjectConfiguration, question: EvalQuestion) -> EvalQuestion:
    """
    Ask a question to the LLM and RAG client.

    :param config: The project configuration.
    :param question: The question to ask.
    :return: An EvalQuestion object containing the question and answers.
    """
    llm_client = setup_llm(max_tokens=2000)

    vectorstore = cast(
        PGVector,
        setup_vectorstore(config.llm.collection, vectorstore_connection(config.db)),
    )
    rag_client = get_retrieval_chain(vectorstore, llm_client, config.llm)
    return EvalQuestion(
        id=question.id,
        question=question.question,
        llm_answer=EvalAnswer(answer=llm_client.invoke(question.question).text()),
        rag_answer=EvalAnswer(answer=rag_client.invoke(question.question)),
    )


def get_precision_eval_prompt(question: str, answer: str) -> str:
    """
    Prompt for evaluating the precision of the answers. Precision is defined as 
    how exactly and concisely the answer addresses the question, avoiding unnecessary 
    or vague information.

    :param question: The question asked.
    :param answer: The answer to evaluate.
    :return: A formatted string for the precision evaluation prompt.
    """
    return (
        "Evaluate the **precision** of the following answer from 0 (low) to 10 (high):\n\n"
        "- High precision = short, fact-based, directly relevant to the question.\n"
        "- Prefer answers that are clear, specific, and avoid repetition or padding.\n"
        "- Penalize vague wording, excessive background info, or off-topic elaboration.\n"
        "- Avoid rewarding long, explanatory or overly detailed responses.\n"
        "- Provide **only a numeric score (0–10)**. Do not add commentary.\n\n"
        f"**Question:** {question}\n\n"
        f"**Answer:** {answer}\n\n"
        "Score (0–10):"
    )


def get_relevance_eval_prompt(question: str, answer: str) -> str:
    """
    Prompt for evaluating the relevance of the answers. Relevance is defined as how 
    well the answer stays on topic and addresses the specific content of the question.

    :param question: The question asked.
    :param answer: The answer to evaluate.
    :return: A formatted string for the relevance evaluation prompt.
    """
    return (
        "Evaluate the **relevance** of the following answer from 0 (low) to 10 (high):\n\n"
        "- High relevance = the answer addresses the question directly and specifically.\n"
        "- Reward answers that clearly use project-specific terms or known context.\n"
        "- Penalize general lists, background info, or 'I don't know'-style hedging.\n"
        "- Focus on how well the answer stays on-topic and avoids off-track content.\n"
        "- Provide **only a numeric score (0–10)**. No explanation.\n\n"
        f"**Question:** {question}\n\n"
        f"**Answer:** {answer}\n\n"
        "Score (0–10):"
    )


def get_completeness_eval_prompt(question: str, answer: str) -> str:
    """
    Prompt for evaluating the completeness of the answers. Completeness is defined 
    as how fully the answer covers all necessary and relevant aspects of the question.


    :param question: The question asked.
    :param answer: The answer to evaluate.
    :return: A formatted string for the completeness evaluation prompt.
    """
    return (
        "Evaluate the **completeness** of the following answer from 0 (low) to 10 (high):\n\n"
        "- High completeness = the answer contains all **key facts** needed to fully answer the question.\n"
        "- Reward concise answers that still deliver all required information.\n"
        "- Penalize irrelevant side notes, excessive verbosity, or repeated info.\n"
        "- Avoid giving higher scores to overly long, tutorial-style answers.\n"
        "- Provide **only a numeric score (0–10)**. Do not explain the score.\n\n"
        f"**Question:** {question}\n\n"
        f"**Answer:** {answer}\n\n"
        "Score (0–10):"
    )


def eval_answers(obj: EvalQuestion) -> EvalQuestion:
    """
    Evaluate the answers using an LLM.

    :param obj: The EvalQuestion object containing the question and answers.
    :return: The EvalQuestion object with the evaluation scores added.
    """
    llm = setup_llm(max_tokens=2)

    # precision scoring
    obj.llm_answer.precision = float(
        llm.invoke(
            get_precision_eval_prompt(obj.question, obj.llm_answer.answer)
        ).text()
    )
    obj.rag_answer.precision = float(
        llm.invoke(
            get_precision_eval_prompt(obj.question, obj.rag_answer.answer)
        ).text()
    )
    # relevance scoring
    obj.llm_answer.relevance = float(
        llm.invoke(
            get_relevance_eval_prompt(obj.question, obj.llm_answer.answer)
        ).text()
    )
    obj.rag_answer.relevance = float(
        llm.invoke(
            get_relevance_eval_prompt(obj.question, obj.rag_answer.answer)
        ).text()
    )
    # completeness scoring
    obj.llm_answer.completeness = float(
        llm.invoke(
            get_completeness_eval_prompt(obj.question, obj.llm_answer.answer)
        ).text()
    )
    obj.rag_answer.completeness = float(
        llm.invoke(
            get_completeness_eval_prompt(obj.question, obj.rag_answer.answer)
        ).text()
    )

    return obj


def save_to_json(answers: list[EvalQuestion], filename: str) -> None:
    """
    Save the evaluation results to a JSON file.

    :param answers: The list of EvalQuestion objects containing the evaluation results.
    :param filename: The name of the JSON file to save the results to.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([obj.model_dump() for obj in answers], f, indent=2)


def create_md_summary_table(answers: list[EvalQuestion]) -> str:
    """
    Create a markdown summary table of the evaluation results.

    :param answers: The list of EvalQuestion objects containing the evaluation results.
    :return: A formatted string representing the markdown table.
    """
    llm_scores = {
        "precision": sum(obj.llm_answer.precision for obj in answers),
        "relevance": sum(obj.llm_answer.relevance for obj in answers),
        "completeness": sum(obj.llm_answer.completeness for obj in answers),
    }
    rag_scores = {
        "precision": sum(obj.rag_answer.precision for obj in answers),
        "relevance": sum(obj.rag_answer.relevance for obj in answers),
        "completeness": sum(obj.rag_answer.completeness for obj in answers),
    }
    return (
        "| Metric | Sum LLM | Sum RAG | Avg. LLM | Avg. RAG |\n"
        "|--------|---------|---------|----------|----------|\n"
        f"| Precision | {llm_scores['precision']} | {rag_scores['precision']} |  {llm_scores['precision'] / len(answers):.2f} | {rag_scores['precision'] / len(answers):.2f} |\n"
        f"| Relevance | {llm_scores['relevance']} | {rag_scores['relevance']} |  {llm_scores['relevance'] / len(answers):.2f} | {rag_scores['relevance'] / len(answers):.2f} |\n"
        f"| Completeness | {llm_scores['completeness']} | {rag_scores['completeness']} |  {llm_scores['completeness'] / len(answers):.2f} | {rag_scores['completeness'] / len(answers):.2f} |\n"
    )


def save_to_markdown(answers: list[EvalQuestion], filename: str) -> None:
    """
    Save the evaluation results to a markdown file.

    :param answers: The list of EvalQuestion objects containing the evaluation results.
    :param filename: The name of the markdown file to save the results to.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Evaluation Results\n\n")
        f.write("## Score Table\n\n")
        f.write(create_md_summary_table(answers))
        f.write("\n\n")
        for obj in answers:
            f.write(f"## {obj.question}\n\n")
            f.write(create_md_summary_table([obj]))
            f.write("\n\n")
            f.write(f"### LLM Answer\n\n{obj.llm_answer.answer}\n\n")  # type: ignore
            f.write(f"### RAG Answer\n\n{obj.rag_answer.answer}\n\n")  # type: ignore
            f.write("---\n\n")


if __name__ == "__main__":
    config = ProjectConfiguration.load_from_yaml(Path(CONFIG_FILE_NAME))

    answers = []
    for question in tqdm(questions):
        result = ask(config, question)
        result = eval_answers(result)
        answers.append(result)
        save_to_json(answers, "eval.json")
        save_to_markdown(answers, "eval.md")
