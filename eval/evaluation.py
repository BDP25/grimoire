import json
import os
import re
from pathlib import Path
from typing import Any, List

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time

EVAL_FOLDER = Path(__file__).parent
ANSWERS_FILE = EVAL_FOLDER / "answers.json"
SCORES_FILE = EVAL_FOLDER / "scores.md"

BATCH_SIZE = 5  
BATCH_DELAY = 60  

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


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=10, max=60),
    retry=retry_if_exception_type(Exception)
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


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=10, max=60),
    retry=retry_if_exception_type(Exception)
)
def get_comparison_comment(llm: Any, question: str, answer_a: str, answer_b: str, score_a: str, score_b: str) -> str:
    """
    Gets a short reason for rating two answers differently from the LLM, now explicitly referencing the score differences.
    :param llm: the language model instance
    :param question: the question text
    :param answer_a: the first answer to compare
    :param answer_b: the second answer to compare
    :param score_a: the score for answer A
    :param score_b: the score for answer B
    :returns: a short comment explaining the rating difference
    """
    prompt = (
        f"Explain why you rated the following two answers differently, considering the scores of {score_a} for Answer A and {score_b} for Answer B.\n\n"
        f"Question:\n{question}\n\n"
        f"Answer A:\n{answer_a}\n\n"
        f"Answer B:\n{answer_b}\n\n"
        f"Reason (1-2 sentences):"
    )
    response = llm.invoke(prompt)
    return extract_content(response)



def load_answers_from_json() -> list[dict[str, str]]:
    """
    Loads the answers from a JSON file for evaluation.
    :returns: a list of dictionaries, each containing question and answers
    """
    with open(ANSWERS_FILE, encoding="utf-8") as f:
        return json.load(f)


def evaluate_batch(llm: Any, batch: List[dict]) -> List[str]:
    """
    Evaluates a batch of questions and answers using the LLM.
    :param llm: the language model instance
    :param batch: list of dictionaries, each containing a question and two answers to evaluate
    :returns: list of formatted evaluation results
    """
    results = []
    for entry in batch:
        question_id = entry["id"]
        question_text = entry["question"]
        answer_a = entry["answer_a"]
        answer_b = entry["answer_b"]

        # Evaluating scores for both answers
        score_a = evaluate_answer(llm, question_text, answer_a)
        score_b = evaluate_answer(llm, question_text, answer_b)
        
        # Getting the comparison comment considering the scores
        comment = get_comparison_comment(llm, question_text, answer_a, answer_b, score_a, score_b)

        results.append(
            f"| {question_id} | {question_text} | {score_a} | {score_b} | {comment} |"
        )
    return results


def evaluate_scores() -> None:
    """
    Evaluates all answers using the LLM and writes the results to a markdown file.
    :returns: None
    """
    data = load_answers_from_json()
    scores = [
        "# Evaluation Scores\n",
        "| ID | Question | Score A | Score B | Comment |",
        "|----|----------|---------|---------|---------|",
    ]

    llm = setup_llm()

    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i:i + BATCH_SIZE]

        batch_results = evaluate_batch(llm, batch)

        scores.extend(batch_results)

        if i + BATCH_SIZE < len(data):
            print(f"Processed batch {i // BATCH_SIZE + 1}. Waiting {BATCH_DELAY} seconds before next batch.")
            time.sleep(BATCH_DELAY)

    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(scores))

    print(f"Scoring completed!\nScores saved: {SCORES_FILE}")


if __name__ == "__main__":
    evaluate_scores()
