# Interactive quiz system, fifth version
# Make a list with the questions and correct answers
# Allow the user to choose the option by its label
# Improve the look and usability, keep track of correct answers

from string import ascii_lowercase


questions = [
    {"question": "What is the capital of France?", "answer": "Paris", "options": ["Toulouse", "Nice", "Avignon"]},
    {"question": "What is the capital of Germany?", "answer": "Berlin", "options": ["Hamburg", "Munich", "Frankfurt"]},
    {"question": "The last Supper was painted by which artist?", "answer": "da Vinci", "options": ["Picasso", "Van Gogh", "Monet"]}
]

num_correct = 0

for num, question_data in enumerate(questions, start=1):
    question = question_data["question"]
    correct_answer = question_data["answer"]
    answers = [correct_answer] + question_data["options"]
    print(f"\nQuestion {num}: {question}")

    sorted_answers = sorted(answers)
    labeled_answers = dict(zip(ascii_lowercase, sorted_answers))


    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")

    answer_label = input("Choice? ").lower()
    answer = labeled_answers.get(answer_label)

    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer}', not {answer!r}.")

print(f"\nYou got {num_correct} out of {len(questions)} questions correct.")