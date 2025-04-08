import json
import subprocess
from pathlib import Path

# Paths
EVAL_FOLDER = Path(__file__).parent
QUESTIONS_FILE = (
    EVAL_FOLDER / "questions_test.json"
)  # TODO: update to "questions.json" for final test
RESULTS_TABLE_FILE = EVAL_FOLDER / "results.md"
FULL_ANSWERS_FILE = EVAL_FOLDER / "full_answers.md"


def load_questions() -> list[dict[str, str]]:
    """Loads questions from the JSON file."""
    with open(QUESTIONS_FILE, encoding="utf-8") as file:
        data = json.load(file)
    return data["questions"]


def ask_question_with_grim(question_text: str, skip_rag: bool = False) -> str:
    """Asks the Grimoire CLI for an answer, ensuring UTF-8 output encoding."""
    cmd = ["grim", "ask", question_text]
    if skip_rag:
        cmd.append("--skip-rag")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        check=True,
    )

    # Clean output by removing unnecessary prefixes
    answer = result.stdout.strip().replace("Grimoire 🔮: ", "")
    return answer


def truncate_answer(answer: str, length: int = 100) -> str:
    """Truncates long answers and appends a reference to the full answer."""
    return answer[:length] + "..." if len(answer) > length else answer


def run_evaluation() -> None:
    """Runs the evaluation and stores results in a readable format."""
    questions = load_questions()
    table_results = []
    full_answers = ["# Evaluation\n"]

    for q in questions:
        question_text = q["question"]
        answer_with_rag = ask_question_with_grim(question_text)
        answer_without_rag = ask_question_with_grim(question_text, skip_rag=True)

        # Store full answers separately
        full_answers.append(
            f"## Q{q['id']}: {question_text}\n\n### LLM Only:\n{answer_without_rag}\n\n### LLM + RAG:\n{answer_with_rag}\n\n---\n"
        )

        # Truncate answers for table readability
        short_answer_without_rag = truncate_answer(answer_without_rag)
        short_answer_with_rag = truncate_answer(answer_with_rag)

        table_results.append(
            f"| {q['id']} | {question_text} | {short_answer_without_rag} | {short_answer_with_rag} |"
        )

    # Write markdown table
    with open(RESULTS_TABLE_FILE, "w", encoding="utf-8") as file:
        file.write("| ID | Question | Answer (LLM Only) | Answer (LLM + RAG) |\n")
        file.write("|----|----------|------------------|-------------------|\n")
        file.write("\n".join(table_results))

    # Write full answers separately
    with open(FULL_ANSWERS_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(full_answers))

    print(
        f"Evaluation completed!\n Table saved: {RESULTS_TABLE_FILE}\n Full answers saved: {FULL_ANSWERS_FILE}"
    )


if __name__ == "__main__":
    run_evaluation()
