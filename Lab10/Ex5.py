# Save the dictionary of quiz questions to a JSON file
import json

questions = [
    {
        "question": "What holiday is during the month of October?",
        "answer": "Halloween",
        "options": ["Christmas", "Thanksgiving", "New Year's Day"],
        "explanation": "Halloween is celebrated in October.",
    },
    {
        "question": "What is the capital of Hawaii?",
        "answer": "Honolulu",
        "options": ["Waikiki", "Waimea", "Waipahu"],
        "explanation": "Honolulu is the capital city of Hawaii.",
    },
    {
        "question": "What is the largest ocean on Earth?",
        "answer": "Pacific Ocean",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
        "explanation": "The Pacific Ocean is the largest ocean on Earth.",
    },
    {
        "question": "How many planets are in our solar system?",
        "answer": "8",
        "options": ["7", "9", "10"],
        "explanation": "There are eight planets in our solar system.",
    },
    {
        "question": "What city is The Golden Gate Bridge in?",
        "answer": "San Francisco",
        "options": ["Los Angeles", "San Diego", "San Jose"],
        "explanation": "The Golden Gate Bridge is in San Francisco.",
    },
]


filename = "quiz_questions.json"

# Open the file in write mode and save the dictionary as JSON
with open(filename, "w") as file:
    json.dump(questions, file, indent=4)
