# Interactive quiz system, third version
# Make a list with the questions and correct answers

questions = [
    {"question": "What is the capital of France?", "answer": "Paris", "options": ["Toulouse", "Nice", "Avignon"]},
    {"question": "What is the capital of Germany?", "answer": "Berlin", "options": ["Hamburg", "Munich", "Frankfurt"]},
    {"question": "The last Supper was painted by which artist?", "answer": "da Vinci", "options": ["Picasso", "Van Gogh", "Monet"]}
]

for q in questions:
    correct_answer = q["answer"]
    answer = input(f"{q['question']} ")
    for option in q["options"]:
        print(f"- {option}")

    
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}', not {answer!r}.")