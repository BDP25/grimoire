import json
import os
import re
from pathlib import Path
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

EVAL_FOLDER = Path(__file__).parent
ANSWERS_FILE = EVAL_FOLDER / "answers.json"
SCORES_FILE = EVAL_FOLDER / "scores.md"


def setup_llm() -> BaseChatModel:
    """
    Initializes and returns a default LLM model (Gemini 2.0 Flash).

    :returns: a BaseChatModel instance ready to receive prompts
    """
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    return init_chat_model(
        "google_genai:gemini-2.0-flash",
        api_key=os.getenv("LLM_API_KEY"),
        configurable_fields=None,
        max_tokens=512,
        temperature=0,
    )


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
        f"Score from 0 to 10 based on how accurate and relevant the answer is, "
        f"and also whether the response is concise and focused. "
        f"Long-winded or overly verbose answers should be penalized. "
        f"Prefer answers that are short but contain all key information.\n\n"
        f"Please provide only a numeric score from 0 to 10 (no text), where:\n"
        f"- 10 = perfect: complete, correct, and concise\n"
        f"- 0 = completely wrong or irrelevant\n\n"
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


def load_answers_from_json() -> list[dict[str, str]]:
    with open(ANSWERS_FILE, encoding="utf-8") as f:
        return json.load(f)


def evaluate_scores() -> None:
    data = load_answers_from_json()
    scores = [
        "# Evaluation Scores\n",
        "| ID | Question | Score A | Score B | Comment |",
        "|----|----------|---------|---------|---------|",
    ]

    llm = setup_llm()

    for entry in data:
        question_id = entry["id"]
        question_text = entry["question"]
        answer_a = entry["answer_a"]
        answer_b = entry["answer_b"]

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
            f"| {question_id} | {question_text} | {score_a} | {score_b} | {comment} |"
        )

    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(scores))

    print(f"Scoring completed!\nScores saved: {SCORES_FILE}")


if __name__ == "__main__":
    evaluate_scores()
