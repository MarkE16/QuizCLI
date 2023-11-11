import unittest
from classes.Question import Question
from classes.Quiz import Quiz


class MyTestCase(unittest.TestCase):
    def test_adding_question_should_succeed(self):
        quiz = Quiz(test_object=True)

        quiz.addQuestion(Question("What is 1 + 1?", "2"))

        self.assertEqual(1, quiz.getNumberOfQuestions())

    def test_removing_question_should_succeed(self):
        quiz = Quiz(test_object=True)

        question = Question("What is 1 + 1?", "2")

        quiz.addQuestion(question)

        self.assertEqual(quiz.getNumberOfQuestions(), 1)

        quiz.removeQuestion(question)

        self.assertEqual(quiz.getNumberOfQuestions(), 0)

    def test_adding_question_should_fail(self):
        quiz = Quiz(test_object=True)

        with self.assertRaises(TypeError):
            quiz.addQuestion()
            quiz.addQuestion(None)
            quiz.addQuestion("What is 1 + 1?")
            quiz.addQuestion(1)
            quiz.addQuestion(1.0)
            quiz.addQuestion(True)

    def test_removing_question_should_fail(self):
        quiz = Quiz(test_object=True)

        with self.assertRaises(TypeError):
            quiz.removeQuestion()
            quiz.removeQuestion(None)
            quiz.removeQuestion("What is 1 + 1?")
            quiz.removeQuestion(1)
            quiz.removeQuestion(1.0)
            quiz.removeQuestion(True)

    def test_creating_question_with_empty_fields_or_null_values_should_fail(self):
        with self.assertRaises(TypeError):
            Question("What is 1 + 1?")
            Question("What is 1 + 1?", None)
            Question(None, "2")
            Question(None, None)
            Question()



if __name__ == '__main__':
    unittest.main()
