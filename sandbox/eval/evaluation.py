from run import load_questions, ask_question_with_grim
from pathlib import Path
import re

EVAL_FOLDER = Path(__file__).parent
SCORES_FILE = EVAL_FOLDER / "scores.md"


def evaluate_scores() -> None:
    """Compares LLM and LLM+RAG answers using an LLM and writes scores to a markdown file."""
    questions = load_questions()
    scores = [
        "# Evaluation Scores\n",
        "| ID | Question | Score (LLM Only) | Score (LLM + RAG) | Comment |",
        "|----|----------|------------------|-------------------|---------|"
    ]

    for q in questions:
        question_text = q["question"]
        answer_a = ask_question_with_grim(question_text, skip_rag=True)
        answer_b = ask_question_with_grim(question_text, skip_rag=False)

        # Construct prompt for evaluation
        eval_prompt = (
            f"Evaluate the two answers on a scale from 0 to 10:\n"
            f"- 10 means the answer is perfect.\n"
            f"- 0 means the answer is completely useless or irrelevant.\n\n"
            f"Question: \"{question_text}\"\n\n"
            f"Answer A (LLM Only): {answer_a}\n\n"
            f"Answer B (LLM + RAG): {answer_b}\n\n"
            f"Return the scores for both answers in the following format:\n"
            f"- Score (LLM Only): <score from 0 to 10>\n"
            f"- Score (LLM + RAG): <score from 0 to 10>\n"
            f"- Comment: <short explanation of the scores>"
        )
        evaluation = ask_question_with_grim(eval_prompt, skip_rag=True)

        # Parse LLM response using regex to extract the scores and comments
        score_a = "?"
        score_b = "?"
        comment = ""

        score_a_match = re.search(r"Score \(LLM Only\):\s*([0-9](?:\.\d{1,2})?)", evaluation)
        score_b_match = re.search(r"Score \(LLM \+ RAG\):\s*([0-9](?:\.\d{1,2})?)", evaluation)
        comment_match = re.search(r"Comment:\s*(.*)", evaluation)

        if score_a_match:
            score_a = score_a_match.group(1)
        if score_b_match:
            score_b = score_b_match.group(1)
        if comment_match:
            comment = comment_match.group(1).strip()

        # Safety fallback in case the score is invalid
        try:
            float(score_a)
            float(score_b)
        except ValueError:
            score_a = score_b = "?"

        scores.append(
            f"| {q['id']} | {question_text} | {score_a} | {score_b} | {comment} |"
        )

    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(scores))

    print(f"Scoring completed!\n Scores saved: {SCORES_FILE}")


if __name__ == "__main__":
    evaluate_scores()
