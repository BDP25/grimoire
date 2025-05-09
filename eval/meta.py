from pydantic import BaseModel


class EvalAnswer(BaseModel):
    answer: str
    precision: float = 0.0
    relevance: float = 0.0


class EvalQuestion(BaseModel):
    id: int
    question: str
    llm_answer: EvalAnswer | None = None
    rag_answer: EvalAnswer | None = None
