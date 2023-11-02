import uuid

class Question:
    def __init__(self, question: str, answer: str) -> None:
        self.question: str = question
        self.answer: str = answer
        self.id: str = str(uuid.uuid4())

    def __str__(self):
        return (
            f"\nQuestion: {self.question}\n" +
            f"Answer: {self.answer}\n"
        )

    def __repr__(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "id": self.id
        }
