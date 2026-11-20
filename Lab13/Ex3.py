

from html import escape

from flask import Flask, redirect, render_template_string, request, url_for
from markupsafe import Markup


app = Flask(__name__)

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>{{ title }} | Kadie's Quiz</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root { color-scheme: light; font-family: Arial, sans-serif; color: #202738; background: #f3f5fb; }
        body { margin: 0; }
        header { padding: 1rem 2rem; background: #273469; color: white; }
        header a { color: white; text-decoration: none; }
        nav { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: .75rem; }
        main { max-width: 760px; margin: 2.5rem auto; padding: 2rem; background: white; border-radius: 14px; box-shadow: 0 8px 28px #20273818; }
        .button, button { display: inline-block; border: 0; border-radius: 8px; padding: .8rem 1rem; background: #4b5fc1; color: white; text-decoration: none; font-size: 1rem; cursor: pointer; }
        .secondary { background: #e9ecf8; color: #273469; }
        .choice { display: block; margin: .8rem 0; padding: .9rem; border: 1px solid #dce1ed; border-radius: 8px; }
        .error { color: #a32121; }
        .success { color: #176b3a; }
        footer { text-align: center; padding: 1rem; color: #667085; }
    </style>
</head>
<body>
    <header>
        <a href="{{ url_for('index') }}"><strong>Kadie's Quiz Game</strong></a>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('quiz') }}">Take the quiz</a>
            <a href="{{ url_for('instructions') }}">Instructions</a>
            <a href="{{ url_for('about') }}">About</a>
        </nav>
    </header>
    <main>
        <h1>{{ title }}</h1>
        {{ body }}
    </main>
    <footer>Flask quiz-game skeleton</footer>
</body>
</html>"""

QUIZ_QUESTION = "What is the capital of Hawaii?"
QUIZ_ANSWERS = ("Honolulu", "Waikiki", "Waimea", "Waipahu")
CORRECT_ANSWER = "Honolulu"


def render_page(title, body):
	"""Render shared page layout with authored HTML content."""
	return render_template_string(PAGE_TEMPLATE, title=title, body=Markup(body))


@app.route("/")
def index():
	"""Show the quiz game's landing page."""
	return render_page(
		"Welcome",
		"""
		<p>Test your knowledge with a short multiple-choice quiz.</p>
		<p>This is the starting skeleton. Add more questions, scoring, and saved high scores as the game grows.</p>
		<p><a class="button" href="/quiz">Take the quiz</a>
		<a class="button secondary" href="/instructions">How to play</a></p>
		""",
	)


@app.route("/instructions")
def instructions():
	"""Display instructions for the mock quiz."""
	return render_page(
		"Instructions",
		"""
		<ol>
		    <li>Choose <strong>Take the quiz</strong> from the navigation.</li>
		    <li>Select one answer for the sample question.</li>
		    <li>Submit your answer to see the result.</li>
		</ol>
		<p>This skeleton currently demonstrates one question; additional questions and randomized choices can be added later.</p>
		<p><a class="button" href="/quiz">Start the quiz</a></p>
		""",
	)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
	"""Display a sample question and accept one multiple-choice response."""
	if request.method == "POST":
		answer = request.form.get("answer", "")
		if answer not in QUIZ_ANSWERS:
			return render_quiz("Please select one of the listed answers.")
		return redirect(url_for("results", answer=answer))
	return render_quiz()


def render_quiz(error_message=""):
	"""Render the sample quiz question, optionally with an input error."""
	error_html = f'<p class="error">{escape(error_message)}</p>' if error_message else ""
	choices = "".join(
		f'<label class="choice"><input type="radio" name="answer" value="{escape(answer, quote=True)}" required> '
		f"{escape(answer)}</label>"
		for answer in QUIZ_ANSWERS
	)
	return render_page(
		"Question 1",
		f"""
		{error_html}
		<form method="post" action="/quiz">
		    <fieldset>
		        <legend>{escape(QUIZ_QUESTION)}</legend>
		        {choices}
		    </fieldset>
		    <p><button type="submit">Submit answer</button></p>
		</form>
		""",
	)


@app.route("/results")
def results():
	"""Show feedback for the submitted sample answer."""
	answer = request.args.get("answer", "")
	if answer not in QUIZ_ANSWERS:
		return render_page(
			"Quiz results",
			'<p>No answer was submitted yet.</p><p><a class="button" href="/quiz">Take the quiz</a></p>',
		)
	if answer == CORRECT_ANSWER:
		feedback = '<p class="success">Correct! Honolulu is the capital of Hawaii.</p>'
		result_text = "Score: 1 out of 1"
	else:
		feedback = f'<p class="error">Not quite. The correct answer is {escape(CORRECT_ANSWER)}.</p>'
		result_text = "Score: 0 out of 1"
	return render_page(
		"Quiz results",
		f"""
		{feedback}
		<p>{result_text}</p>
		<p><a class="button" href="/quiz">Try again</a>
		<a class="button secondary" href="/">Return home</a></p>
		""",
	)


@app.route("/about")
def about():
	"""Describe the prototype and its next development steps."""
	return render_page(
		"About this quiz",
		"""
		<p>This Flask app is a navigable prototype for a quiz game.</p>
		<p>The page structure is ready to expand with a question bank, randomized question order, a running score, and a high-score feature.</p>
		""",
	)


if __name__ == "__main__":
	app.run(debug=True)
