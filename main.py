import typer
import json
from random import randint
from json import JSONDecodeError

cmd = typer.Typer()
questions = []

"""
The `questionExists` function.

This function is used to determine whether or not a question already exists in the current list.

:param: question - The question to locate.
:returns: A tuple containing a boolean and integer. The boolean determines if the question was found. If found, the
integer returned will be the question's location in the list, -1 otherwise.
"""


def questionExists(question: str) -> tuple[bool, int]:
    for idx in range(len(questions)):
        if questions[idx]['question'] == question:
            return True, idx
    return False, -1


def printResults(user_answer, current_question_answer) -> bool:
    returnResult = False
    if user_answer != current_question_answer:
        print("Incorrect.")
    else:
        print("Correct.")
        returnResult = True
    print("The correct answer was: \"" + current_question_answer + "\".\nYour answer was: \"" + user_answer + "\".")
    return returnResult

def saveData():
    with open("./data/questions.json", "w") as f:
        json.dump(questions, f, indent=2)

@cmd.command(help="Lists out your current questions.")
def q_list():
    if len(questions) == 0:
        print("You have no questions for the quiz.")
        return

    print("REVIEW QUESTIONS\n")

    for q in questions:
        print(
            "QUESTION: " + q['question'] + "\n" +
            "ANSWER: " + q['answer']
        )

@cmd.command(no_args_is_help=True, help="Creates a question. If the delete flag is passed, the question will be deleted (if found).")
def question(question: str, answer: str, add: bool=True, delete: bool=False):

    qestion_exists, location = questionExists(question)
    if add:
        if qestion_exists:
            print("You already have this question.")
            return
        questions.append({
            "question": question,
            "answer": answer,
            "id": len(questions) + 1
        })
        saveData()
        print("Question added.")
    elif delete:
        if qestion_exists:
            questions.pop(location)
            print("Question removed.")
            saveData()
            return
        print("Question doesn't exist.")

@cmd.command(help="Starts a quiz session.")
def start():
    progress = {
        "correct": 0,
        "incorrect": 0
    }

    questions_answered = 0
    questions_answered_idxs = []

    print("Tip! Press `CTRL + C` (`CMD + C` on a Mac) to quit.")
    while questions_answered < len(questions):
        selected_question_idx: int

        while True:
            selected_question_idx = randint(0, len(questions) - 1)
            if selected_question_idx not in questions_answered_idxs:
                break

        selected_question = questions[selected_question_idx]['question']
        selected_question_answer = questions[selected_question_idx]['answer']
        print(
            f"QUESTION #{questions_answered + 1}:\n" +
            f"\"{selected_question}\"\n"
        )
        answer = str(input("Enter your answer: "))

        correct = printResults(answer, selected_question_answer)

        if correct:
            progress['correct'] += 1
        else:
            progress['incorrect'] += 1

        questions_answered = progress['correct'] + progress['incorrect']
        questions_answered_idxs.append(selected_question_idx)
    print("\nQuiz Over! Results:")

    print(
        "Correct Answers: " + str(progress['correct']) + "\n" +
        "Incorrect Answers: " + str(progress['incorrect']) + "\n" +
        "Percentage: " + str(((progress['correct'] / questions_answered) * 100)) + "%\n"
    )



if __name__ == "__main__":

    try:
        with open("./data/questions.json") as f:
            questions = json.load(f)
    except JSONDecodeError:
        pass

    cmd()
