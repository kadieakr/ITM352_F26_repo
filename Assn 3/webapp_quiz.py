"""A small Flask version of the Assignment 1 quiz."""

import json
import os
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for


ASSIGNMENT_1 = Path(__file__).resolve().parent.parent / "Assn 1"
QUESTIONS_FILE = ASSIGNMENT_1 / "questions.json"
HIGH_SCORE_FILE = ASSIGNMENT_1 / "high_score.txt"
QUESTIONS = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))

app = Flask(__name__, template_folder="quiz_templates")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-development-key")
app.permanent_session_lifetime = timedelta(days=30)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def get_high_score():
    """Read Assignment 1's saved high score."""
    try:
        return int(HIGH_SCORE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0


def save_result(quiz_data):
    """Save a completed attempt in the session and update the high score."""
    score = quiz_data["score"]
    total = len(quiz_data["questions"])
    old_record = get_high_score()
    new_record = score > old_record
    if new_record:
        try:
            HIGH_SCORE_FILE.write_text(str(score), encoding="utf-8")
        except OSError:
            app.logger.exception("Could not save the high score.")
            new_record = False

    completed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    result = {
        "score": score,
        "total": total,
        "answers": quiz_data["answers"],
        "completed_at": completed_at,
        "high_score": max(score, old_record) if new_record else old_record,
        "new_record": new_record,
    }
    history = session.get("history", [])
    history.append({"score": score, "total": total, "completed_at": completed_at})
    session["history"] = history[-20:]
    session["result"] = result
    session.pop("quiz", None)


@app.route("/", methods=["GET", "POST"])
def home():
    """Ask new players for a name or show returning players their scores."""
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name or len(name) > 40:
            error = "Enter a name up to 40 characters long."
        else:
            session["name"] = name
            session.permanent = True
            return redirect(url_for("home"))

    return render_template(
        "index.html",
        name=session.get("name"),
        history=session.get("history", []),
        latest=session.get("result"),
        high_score=get_high_score(),
        error=error,
    )


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Show a randomized question, check its answer, and track progress."""
    if not session.get("name"):
        return redirect(url_for("home"))

    quiz_data = session.get("quiz")
    if not quiz_data:
        question_ids = random.sample(range(len(QUESTIONS)), k=min(5, len(QUESTIONS)))
        quiz_data = {"questions": [], "answers": [], "score": 0}
        for question_id in question_ids:
            choices = [QUESTIONS[question_id]["answer"], *QUESTIONS[question_id]["options"]]
            random.shuffle(choices)
            quiz_data["questions"].append({"id": question_id, "choices": choices})
        session["quiz"] = quiz_data

    position = len(quiz_data["answers"])
    total = len(quiz_data["questions"])
    if request.method == "POST":
        item = quiz_data["questions"][position]
        question = QUESTIONS[item["id"]]
        selected = request.form.get("answer", "")
        if selected not in item["choices"]:
            return render_quiz(quiz_data, error="Select one of the listed answers."), 400

        correct = selected == question["answer"]
        quiz_data["score"] += int(correct)
        quiz_data["answers"].append({
            "question": question["question"],
            "selected": selected,
            "correct_answer": question["answer"],
            "explanation": question.get("explanation", ""),
            "correct": correct,
        })
        session["quiz"] = quiz_data
        if len(quiz_data["answers"]) == total:
            save_result(quiz_data)
            return redirect(url_for("result"))
        return redirect(url_for("quiz"))

    return render_quiz(quiz_data)


def render_quiz(quiz_data, error=None):
    """Render the current question and progress bar."""
    position = len(quiz_data["answers"])
    item = quiz_data["questions"][position]
    return render_template(
        "quiz.html",
        name=session["name"],
        question=QUESTIONS[item["id"]],
        choices=item["choices"],
        number=position + 1,
        total=len(quiz_data["questions"]),
        progress=round(position / len(quiz_data["questions"]) * 100),
        feedback=quiz_data["answers"][-1] if quiz_data["answers"] else None,
        error=error,
    )


@app.route("/result")
def result():
    """Show the completed quiz score and feedback."""
    if not session.get("name") or not session.get("result"):
        return redirect(url_for("home"))
    return render_template("result.html", name=session["name"], result=session["result"])


@app.route("/restart", methods=["POST"])
def restart():
    """Start a new quiz and keep the player's score history."""
    session.pop("quiz", None)
    return redirect(url_for("quiz"))


@app.route("/change-name", methods=["POST"])
def change_name():
    """Clear the current browser session."""
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

