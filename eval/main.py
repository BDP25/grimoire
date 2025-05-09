import json
from pathlib import Path
from typing import cast

from langchain_postgres import PGVector
from meta import EvalAnswer, EvalQuestion
from questions import questions

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    ProjectConfiguration,
)
from grimoire.helpers.llm import setup_llm
from grimoire.helpers.retriever import get_retrieval_chain
from grimoire.helpers.vectorstore import setup_vectorstore, vectorstore_connection


def ask(config: ProjectConfiguration, question: EvalQuestion) -> EvalQuestion:
    llm_client = setup_llm()

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


def save_to_json(answers: list[EvalQuestion], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([obj.model_dump() for obj in answers], f, indent=2)


def save_to_markdown(answers: list[EvalQuestion], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Evaluation Results\n\n")
        for obj in answers:
            f.write(f"## {obj.question}\n\n")
            f.write(f"### LLM Answer\n\n{obj.llm_answer.answer}\n\n")  # type: ignore
            f.write(f"### RAG Answer\n\n{obj.rag_answer.answer}\n\n")  # type: ignore
            f.write("---\n")


if __name__ == "__main__":
    config = ProjectConfiguration.load_from_yaml(Path(CONFIG_FILE_NAME))
    answers = []
    for question in questions:
        result = ask(config, question)
        answers.append(result)
        break

    # save to json
    save_to_json(answers, "eval.json")
    save_to_markdown(answers, "eval.md")
