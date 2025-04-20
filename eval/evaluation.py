import re
from pathlib import Path
from typing import Any

from run import ask_question_with_grim, load_questions

from grimoire.helpers.rag import setup_llm

EVAL_FOLDER = Path(__file__).parent
SCORES_FILE = EVAL_FOLDER / "scores.md"


def extract_score(text: str) -> str:
    """
    Extract a number between 0 and 10 from the LLM response.

    :param text: the LLM's response text
    :returns: a numeric score as a string or "?" if invalid
    """
    if match := re.search(r"\b(\d{1,2})\b", text):
        score = int(match.group(1))
        if 0 <= score <= 10:
            return str(score)
    return "?"


def extract_content(response: Any) -> str:
    """
    Extracts string content from LLM response safely.

    :param response: the LLM's response object
    :returns: the extracted content as a string
    """
    content = getattr(response, "content", "")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list) and content:
        # take the first string from the list (if any)
        for item in content:
            if isinstance(item, str):
                return item.strip()
            if isinstance(item, dict) and "text" in item:
                return str(item["text"]).strip()
    return ""


def build_score_prompt(question: str, answer: str) -> str:
    """
    Builds a scoring prompt for the LLM.

    :param question: the input question
    :param answer: the answer to evaluate
    :returns: the full prompt string for scoring
    """
    return (
        f"Evaluate the following answer to the question. "
        f"Please provide only a numeric score from 0 to 10, where 10 is perfect and 0 is completely wrong. "
        f"Respond with the number only.\n\n"
        f"Question:\n{question}\n\n"
        f"Answer:\n{answer}\n\n"
        f"Score:"
    )


def evaluate_answer(llm: Any, question: str, answer: str) -> str:
    """
    Evaluates a single answer using the LLM and extracts the score.

    :param llm: the language model instance
    :param question: the question text
    :param answer: the answer to be evaluated
    :returns: the score as a string
    """
    prompt = build_score_prompt(question, answer)
    response = llm.invoke(prompt)
    return extract_content(response)


def evaluate_scores() -> None:
    """
    Compares Answer A and B without disclosing origin; returns scores via LLM.

    :returns: None
    """
    questions = load_questions()
    scores = [
        "# Evaluation Scores\n",
        "| ID | Question | Score A | Score B | Comment |",
        "|----|----------|---------|---------|---------|",
    ]

    llm = setup_llm()

    for q in questions:
        question_text = q["question"]
        answer_a = ask_question_with_grim(question_text, skip_rag=True)
        answer_b = ask_question_with_grim(question_text, skip_rag=False)

        score_a = evaluate_answer(llm, question_text, answer_a)
        score_b = evaluate_answer(llm, question_text, answer_b)

        comment_prompt = (
            f"Give a short reason (1-2 sentences) why you would rate the following two answers differently.\n\n"
            f"Question:\n{question_text}\n\n"
            f"Answer A:\n{answer_a}\n\n"
            f"Answer B:\n{answer_b}\n\n"
            f"Reason:"
        )
        comment = extract_content(llm.invoke(comment_prompt))

        scores.append(
            f"| {q['id']} | {question_text} | {score_a} | {score_b} | {comment} |"
        )

    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(scores))

    print(f"Scoring completed!\nScores saved: {SCORES_FILE}")


if __name__ == "__main__":
    evaluate_scores()
