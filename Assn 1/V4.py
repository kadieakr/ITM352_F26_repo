# Interactive quiz system, second version
# Make a list with the questions and correct answers
# Allow the user to choose the option by its label

questions = [
    {"question": "What is the capital of France?", "answer": "Paris", "options": ["Toulouse", "Nice", "Avignon"]},
    {"question": "What is the capital of Germany?", "answer": "Berlin", "options": ["Hamburg", "Munich", "Frankfurt"]},
    {"question": "The last Supper was painted by which artist?", "answer": "da Vinci", "options": ["Picasso", "Van Gogh", "Monet"]}
]

for question, answers in questions.items():
    correct_answer = answers[0]
    sorted_answers = sorted(answers)

    for label, answer in enumerate(sorted_answers, start=1):
        print(f"{label}. {answer}")

    answer_label = int(input(f"(question)"))
    answer = sorted_answers[answer_label - 1]

    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}', not {answer!r}.")