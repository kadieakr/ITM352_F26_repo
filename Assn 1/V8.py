# Interactive quiz system, eighth version
# Make a list of question dictionaries with the correct answer and distractors.
# Allow the user to choose the option by its label.
# Improve the look and usability. Keep track of correct answers.
# Randomize the order of the questions and the order of the answers for each question.
# Refactor the code to use functions.

from string import ascii_lowercase
import random
import json

with open("questions.json", "r") as question_file:
    questions = json.load(question_file)


HIGH_SCORE_FILE = "high_score.txt"


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0


def update_high_score(score):
    best_score = load_high_score()
    if score > best_score:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
        print(f"\n🎉 New high score! {score} correct!")


NUM_QUESTIONS_PER_QUIZ = 5


def prepare_questions(questions, num_questions):
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)


def get_answer(question, alternatives):
    labeled_answers = dict(zip(ascii_lowercase, alternatives))

    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")

    while (answer_label := input("Choice? ").lower()) not in labeled_answers:
        print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}.")

    return labeled_answers[answer_label]


def ask_question(question_data):
    question = question_data["question"]
    correct_answer = question_data["answer"]
    explanation = question_data.get("explanation", "No explanation available.")
    alternatives = [correct_answer] + question_data["options"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    print(f"\nQuestion: {question}")
    answer = get_answer(question, ordered_alternatives)

    if answer == correct_answer:
        print("Correct!")
        print(f"Why: {explanation}")
        return 1
    else:
        print(f"The answer is '{correct_answer}', not {answer!r}.")
        return 0


# Main program logic starts here
quiz_questions = prepare_questions(questions, NUM_QUESTIONS_PER_QUIZ)

num_correct = 0

# Main Loop
for num, question_data in enumerate(quiz_questions, start=1):
    print(f"\nQuestion {num}")
    num_correct += ask_question(question_data)

print(f"\nYou got {num_correct} correct.")
update_high_score(num_correct)