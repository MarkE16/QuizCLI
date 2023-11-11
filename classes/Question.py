import uuid

class Question:
    def __init__(self, question: str, answer: str, answered: bool = False, answered_correctly: bool = False) -> None:
        if question is None or answer is None:
            raise TypeError("Question and answer cannot be None.")
        self.question: str = question
        self.answer: str = answer
        self.id: str = str(uuid.uuid4())
        self.answered: bool = answered
        self.answered_correctly: bool = answered_correctly

    def set_answered(self, answered: bool) -> None:
        self.answered = answered

    def set_answered_correctly(self, answered_correctly: bool) -> None:
        self.answered_correctly = answered_correctly

    def __str__(self) -> str:
        return (
            f"\nQuestion: {self.question}\n" +
            f"Answer: {self.answer}\n"
        )
