import os

from classes.Question import Question
from json import dump, load, JSONDecodeError
from uuid import uuid4
from os import remove, makedirs, removedirs
from os.path import exists


class Quiz:
    def __init__(self, questions: list[Question] = None, test_object: bool = False) -> None:
        if questions is None:
            questions = []
        self.questions: list[Question] = questions
        """
        This value is used to determine whether or not to delete the saved questions file when the Quiz object is
        destructed. This only exists for testing purposes.
        """
        self.test_object: bool = test_object

        self.saved_questions_location: str

        if test_object:
            if not exists("./test_data"):
                makedirs("./test_data")
            self.saved_questions_location = "./test_data/TEST_q_" + str(uuid4()) + ".json"
            f = open(self.saved_questions_location, "x")
            f.close()
        else:
            if exists("./data"):
                for file in os.listdir("./data"):
                    if file.endswith(".json") and file.startswith("q_"):
                        self.saved_questions_location = "./data/" + file
                        break
            else:
                makedirs("./data")
                self.saved_questions_location = "./data/q_" + str(uuid4()) + ".json"
                f = open(self.saved_questions_location, "x")
                f.close()

    def __del__(self) -> None:
        if self.test_object:
            for file in os.listdir("./test_data"):
                remove("./test_data/" + file)
            removedirs("./test_data")

    def addQuestion(self, question: Question) -> None:
        """
        Adds a question to the array of questions.

        :param question: A Question object.
        :return: `addQuestion` returns None.
        """

        if question.__class__ is not Question:
            raise TypeError(question.__class__.__name__ + " is not a Question object.")
        self.questions.append(question)

    def removeQuestion(self, question: Question) -> None:
        """
        Removes a question from the array of questions.

        :param question: A Question object.
        :return: `removeQuestion` returns None.
        """
        if question.__class__ is not Question:
            raise TypeError(question.__class__.__name__ + " is not a Question object.")
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

    def getNumberOfQuestions(self) -> int:
        """
        Returns the number of questions in the array of questions.

        :return: `getNumberOfQuestions` returns an integer.
        """
        return len(self.questions)

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

    def getResults(self) -> dict[str, int]:
        """
        Returns a dictionary containing the number of correct and incorrect answers.

        :return: `getResults` returns a dictionary with the keys `correct` and `incorrect`, both of which containing
        integers.
        """

        correct = len(list(filter((lambda question: question.answered_correctly), self.questions)))

        return {
            "correct": correct,
            "incorrect": self.getTotalAnswered() - correct,
        }

    def save(self) -> None:
        """
        Saves the current array of questions to the external JSON.

        :return: `save` returns None.
        """
        with open(self.saved_questions_location, "w") as f:
            jsonSerialized = list(map((lambda question: question.__dict__), self.questions))
            dump(jsonSerialized, f, indent=2)

    def load(self) -> None:
        """
        Loads the current array of questions from the external JSON.

        :return: `load` returns None.
        """
        with open(self.saved_questions_location, "r") as f:
            jsonDeserialized = []
            try:
                jsonDeserialized = load(f)
            except JSONDecodeError:
                return
            self.questions = list(map((lambda question: Question(question['question'], question['answer'], question['answered'], question['answered_correctly'])), jsonDeserialized))

    def setQuestionsToUnanswered(self) -> None:
        """
        Sets all questions to unanswered.

        :return: `setQuestionsToUnanswered` returns None.
        """
        for question in self.questions:
            question.set_answered(False)
            question.set_answered_correctly(False)
