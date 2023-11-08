import unittest
from classes.Quiz import Quiz
from classes.Question import Question


class MyTestCase(unittest.TestCase):
    def test_adding_question_should_succeed(self):
        quiz = Quiz(test_object=True)

        quiz.addQuestion(Question("What is 1 + 1?", "2"))

        print(quiz.saved_questions_location)

        self.assertEqual(quiz.getNumberOfQuestions(), 1)

    def test_removing_question_should_succeed(self):
        quiz = Quiz(test_object=True)

        question = Question("What is 1 + 1?", "2")

        quiz.addQuestion(question)

        self.assertEqual(quiz.getNumberOfQuestions(), 1)

        quiz.removeQuestion(question)

        self.assertEqual(quiz.getNumberOfQuestions(), 0)


if __name__ == '__main__':
    unittest.main()
