import json
from pathlib import Path

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from typer.testing import CliRunner

from grimoire.main import cli

# Initialize CLI runner for testing and evaluation
runner = CliRunner()

# Define paths for evaluation assets
EVAL_FOLDER = Path(__file__).parent
QUESTIONS_FILE = EVAL_FOLDER / "questions.json"
FULL_ANSWERS_FILE = EVAL_FOLDER / "full_answers.md"
JSON_ANSWERS_FILE = EVAL_FOLDER / "answers.json"  # For evaluation


def load_questions() -> list[dict[str, str]]:
    """
    Load evaluation questions from the questions.json file.

    :returns: A list of dictionaries containing question IDs and question text.
    """
    with open(QUESTIONS_FILE, encoding="utf-8") as file:
        data = json.load(file)
    return data["questions"]


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=10, max=60),
    retry=retry_if_exception_type(RuntimeError),
)
def query_grimoire_cli(question_text: str, use_rag: bool = True) -> str:
    """
    Invoke the Grimoire CLI using CliRunner to answer a question.

    :param question_text: The input question to ask the CLI.
    :param use_rag: Whether to use RAG (retrieval-augmented generation). If False, the --skip-rag flag is added.
    :returns: The CLI output as a cleaned string (Grimoire prompt removed).
    """
    args = ["ask", question_text]
    if not use_rag:
        args.append("--skip-rag")

    result = runner.invoke(cli, args)

    if result.exit_code != 0:
        raise RuntimeError(f"CLI error:\n{result.output}")

    return result.output.strip().replace(
        "Grimoire 🔮: ", ""
    )  # For scoring remove "Grimoire 🔮:"


def truncate_answer(answer: str, length: int = 100) -> str:
    """
    Truncate long answers for table display and add ellipsis.

    :param answer: The full answer text.
    :param length: The maximum number of characters to retain.
    :returns: A shortened version of the answer with ellipsis if truncated.
    """
    return answer[:length] + "..." if len(answer) > length else answer


def run_evaluation() -> None:
    """
    Run the evaluation process for a set of questions.

    It executes Grimoire CLI queries with and without RAG, collects and saves results
    in Markdown and JSON format.
    """
    questions = load_questions()
    full_answers_md = ["# Evaluation\n"]
    json_answers = []

    for q in questions:
        question_text = q["question"]

        # Ask with and without RAG
        answer_with_rag = query_grimoire_cli(question_text, use_rag=True)
        answer_without_rag = query_grimoire_cli(question_text, use_rag=False)

        # Save full answers for review
        full_answers_md.append(
            f"## Q{q['id']}: {question_text}\n\n"
            f"### LLM Only:\n{answer_without_rag}\n\n"
            f"### LLM + RAG:\n{answer_with_rag}\n\n---\n"
        )

        # Neutral format for JSON (no bias labels)
        json_answers.append(
            {
                "id": q["id"],
                "question": question_text,
                "answer_a": answer_without_rag,
                "answer_b": answer_with_rag,
            }
        )

    # Save full answers separately
    with open(FULL_ANSWERS_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(full_answers_md))

    # Save JSON for scoring
    with open(JSON_ANSWERS_FILE, "w", encoding="utf-8") as file:
        json.dump(json_answers, file, indent=2, ensure_ascii=False)

    print(
        f"Evaluation completed!\n"
        f"Full answers saved: {FULL_ANSWERS_FILE}\n"
        f"JSON saved: {JSON_ANSWERS_FILE}"
    )


if __name__ == "__main__":
    run_evaluation()
