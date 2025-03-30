import argparse

from helpers import setup_llm
from retrieval_chain import build_retrieval_chain, stream_response


def ask_question(question: str, use_retrieval: bool) -> None:
    if use_retrieval:
        print("Using retrieval chain for context...")
        chain = build_retrieval_chain()
        response_generator = stream_response(chain, question)
        response = "".join([chunk for chunk in response_generator if chunk is not None])
    else:
        print("Skipping retrieval process. Asking directly to LLM...")
        llm = setup_llm()
        response = llm.predict(question)

    print("Answer: ", response)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask questions to the system.")
    parser.add_argument("question", type=str, help="The question to ask.")
    parser.add_argument(
        "--skip-retrieval",
        action="store_true",
        help="Skip the retrieval process and ask LLM directly.",
    )
    args = parser.parse_args()
    use_retrieval = not args.skip_retrieval
    ask_question(args.question, use_retrieval)


if __name__ == "__main__":
    main()
