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
    Prompt for evaluating the precision of the answers.

    :param question: The question asked.
    :param answer: The answer to evaluate.
    :return: A formatted string for the evaluation prompt.
    """
    return (
        "Evaluate the precision of the two answers below. Score from 0 to 10 based on how precise "
        "the answers are. Long-winded or overly verbose answers should be penalized. "
        "Assume that the answers were given for a specific context which you are not aware of. "
        "Prefer answers that are short but contain all key information. "
        "Please provide only a numeric score from 0 (low) to 10 (high) with no explanation text.\n\n"
        f"Question: {question}\n\n"
        f"Answer: {answer}\n\n"
        "Score:"
    )


def get_relevance_eval_prompt(question: str, answer: str) -> str:
    """
    Prompt for evaluating the relevance of the answers.

    :param question: The question asked.
    :param answer: The answer to evaluate.
    :return: A formatted string for the evaluation prompt.
    """
    return (
        "Evaluate the relevance of the two answers below. Score from 0 to 10 based on how relevant "
        "the answers are. Long-winded or overly verbose answers should be penalized. "
        "Assume that the answers were given for a specific context which you are not aware of. "
        "Prefer answers that are short but contain all key information. "
        "Please provide only a numeric score from 0 (low) to 10 (high) with no explanation text.\n\n"
        f"Question: {question}\n\n"
        f"Answer: {answer}\n\n"
        "Score:"
    )


def get_completeness_eval_prompt(question: str, answer: str) -> str:
    """
    Prompt for evaluating the completeness of the answers.

    :param question: The question asked.
    :param answer: The answer to evaluate.
    :return: A formatted string for the evaluation prompt.
    """
    return (
        "Evaluate the completeness of the two answers below. Score from 0 to 10 based on how "
        "complete the answers are. Long-winded or overly verbose answers should be penalized. "
        "Assume that the answers were given for a specific context which you are not aware of. "
        "Prefer answers that are short but contain all key information. "
        "Please provide only a numeric score from 0 (low) to 10 (high) with no explanation text.\n\n"
        f"Question: {question}\n\n"
        f"Answer: {answer}\n\n"
        "Score:"
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
