from typer import Typer
from classes.Question import Question
from classes.Quiz import Quiz
from os import system

cmd = Typer()
questions = Quiz()


def printResults(user_answer, current_question_answer) -> None:
    if user_answer != current_question_answer:
        print("Incorrect.")
    else:
        questions.incrementScore()
        print("Correct.")
    print("The correct answer was: \"" + current_question_answer + "\".\nYour answer was: \"" + user_answer + "\".")
    input("Press enter to continue.")


@cmd.command(help="Lists out your current questions.")
def q_list():
    current_questions = questions.getQuestions()
    if len(current_questions) == 0:
        print("You have no questions for the quiz.")
        return

    print("REVIEW QUESTIONS:")

    for q in current_questions:
        print(q)


@cmd.command(no_args_is_help=True,
             help="Creates a question. If the delete flag is passed, the question will be deleted (if found).")
def question(question: str, answer: str, add: bool = True, delete: bool = False):
    doesQuestionExist = questions.getQuestion(question)
    if delete:
        if doesQuestionExist is None:
            print("Question doesn't exist.")
            return
        questions.removeQuestion(doesQuestionExist)
        print("Question removed.")
        questions.save()
    elif add:
        if doesQuestionExist is not None:
            print("You already have this question.")
            return
        questions.addQuestion(Question(question, answer))
        questions.save()
        print("Question added.")


@cmd.command(help="Starts a quiz session.")
def start():
    total_questions = questions.getQuestions()
    length_of_all_questions = len(total_questions)
    questions_answered = questions.getTotalAnswered()

    if length_of_all_questions == 0:
        print("You need questions to start a quiz. Create some using the `question` command.")
        return

    system("cls")  # Clear the screen.


    while questions_answered < length_of_all_questions:
        selected_question = questions.getRandomQuestion()

        while selected_question.answered:
            selected_question = questions.getRandomQuestion()


        print(
            f"QUESTION #{questions_answered + 1}:\n" +
            f"\"{selected_question.question}\"\n"
        )
        answer = str(input("Enter your answer (enter 'end' to end the quiz; 'exit' to quit and save): "))

        if answer == "end":
            break

        if answer == "exit":
            exit(0)

        printResults(answer, selected_question.answer)

        selected_question.answered = True
        questions_answered = questions.getTotalAnswered()
        questions.save()
        system("cls")  # Clear the screen.
    print("\nQuiz Over! Results:")

    progress = questions.getResults()

    print(
        "Correct Answers: " + str(progress['correct']) + "\n" +
        "Incorrect Answers: " + str(progress['incorrect']) + "\n" +
        "Percentage: " + str(round(((progress['correct'] / questions_answered) * 100), 2)) + "%\n"
    )
    questions.setQuestionsToUnanswered()  # All done! Set all questions to unanswered, so they can be answered again.
    questions.save()


if __name__ == "__main__":
    questions.load()

    cmd()
