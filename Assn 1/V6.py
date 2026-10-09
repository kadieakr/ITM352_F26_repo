# Interactive quiz system, sixth version
# Make a list with the questions and correct answers
# Allow the user to choose the option by its label
# Improve the look and usability, keep track of correct answers
# Randomize the order of the questions and the order of the answers for each question.

from string import ascii_lowercase
import random

questions = [
    {"question": "What is the capital of France?", "answer": "Paris", "options": ["Toulouse", "Nice", "Avignon"]},
    {"question": "What is the capital of Germany?", "answer": "Berlin", "options": ["Hamburg", "Munich", "Frankfurt"]},
    {"question": "The last Supper was painted by which artist?", "answer": "da Vinci", "options": ["Picasso", "Van Gogh", "Monet"]}
]
random.shuffle(questions)  # Shuffle the questions

NUM_QUESTIONS_PER_QUIZ = 5
quiz_questions = questions[:NUM_QUESTIONS_PER_QUIZ]

num_correct = 0

for num, question_data in enumerate(quiz_questions, start=1):
    question = question_data["question"]
    correct_answer = question_data["answer"]
    answers = [correct_answer] + question_data["options"]
    print(f"\nQuestion {num}: {question}")

    random.shuffle(answers)  # Shuffle the answers for this question
    labeled_answers = dict(zip(ascii_lowercase, answers))


    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")


    while True:
        answer_label = input("Choice? ").lower()
        if answer_label in labeled_answers:
            break
        print("Invalid choice. Please select a valid option.")

    answer = labeled_answers.get(answer_label)

    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer}', not {answer!r}.")

print(f"\nYou got {num_correct} out of {len(quiz_questions)} questions correct.")