from classes.Question import Question
from json import dump, load, JSONDecodeError


class Quiz:
    def __init__(self, questions: list[Question]=[]) -> None:
        self.questions: list[Question] = questions
        self.score: int = 0

    def addQuestion(self, question: Question) -> None:
        """
        Adds a question to the array of questions.

        :param question: A Question object.
        :return: `addQuestion` returns None.
        """
        self.questions.append(question)

    def removeQuestion(self, question: Question) -> None:
        """
        Removes a question from the array of questions.

        :param question: A Question object.
        :return: `removeQuestion` returns None.
        """
        self.questions.remove(question)

    def getQuestion(self, text: str) -> Question | None:
        """
        Searches through the array of questions for a question with matching text as the `text` parameter.

        :param text: The text of the question to search for.
        :return: `getQuestion` returns a Question object if found, otherwise it returns None.
        """
        for question in self.questions:
            if question.question == text:
                return question
        return None

    def getQuestions(self) -> list[Question]:
        """
        Returns the current array of questions.

        :return: `getQuestions` returns a list of Question objects. If there are no questions, it returns an empty list.
        """
        return self.questions

    def getRandomQuestion(self) -> Question:
        """
        Returns a random question from the array of questions.

        :return: `getRandomQuestion` returns a randomly chosen Question object.
        """
        from random import choice
        return choice(self.questions)

    def getTotalAnswered(self) -> int:
        """
        Returns the total number of questions that have been answered.

        :return: `getTotalAnswered` returns an integer.
        """
        return len(list(filter((lambda question: question.answered), self.questions)))

    def incrementScore(self) -> None:
        """
        Increments the score by 1.

        :return: `incrementScore` returns None.
        """
        self.score += 1

    def getResults(self) -> dict[str, int]:
        """
        Returns a dictionary containing the number of correct and incorrect answers.

        :return: `getResults` returns a dictionary with the keys `correct` and `incorrect`, both of which containing
        integers.
        """
        return {
            "correct": self.score,
            "incorrect": self.getTotalAnswered() - self.score,
        }

    def save(self) -> None:
        """
        Saves the current array of questions to an external JSON called `questions.json`.

        :return: `save` returns None.
        """
        with open("data/questions.json", "w") as f:
            jsonSerialized = list(map((lambda question: question.__dict__), self.questions))
            dump(jsonSerialized, f, indent=2)

    def load(self) -> None:
        """
        Loads the current array of questions from an external JSON called `questions.json`.

        :return: `load` returns None.
        """
        with open("data/questions.json", "r") as f:
            jsonDeserialized = []
            try:
                jsonDeserialized = load(f)
            except JSONDecodeError:
                return
            self.questions = list(map((lambda question: Question(question['question'], question['answer'], question['answered'])), jsonDeserialized))

    def setQuestionsToUnanswered(self) -> None:
        """
        Sets all questions to unanswered.

        :return: `setQuestionsToUnanswered` returns None.
        """
        for question in self.questions:
            question.answered = False
