"""Standalone visual mockup for the Hawaii internships project.

Run this file to preview the page design independently of Ex1.py.
It uses sample listings so it does not need the missing helpers module.
"""

from flask import Flask, render_template_string, request


app = Flask(__name__)

SAMPLE_INTERNSHIPS = [
	{
		"title": "Business Analyst Intern",
		"company": "Pacific Coast Consulting",
		"island": "Oahu",
		"major": "MIS",
		"season": "Summer",
		"deadline": "April 15, 2026",
		"paid": True,
		"description": "Help a local team turn business data into useful recommendations.",
	},
	{
		"title": "Marketing Intern",
		"company": "Aloha Creative Studio",
		"island": "Maui",
		"major": "Marketing",
		"season": "Fall",
		"deadline": "June 1, 2026",
		"paid": True,
		"description": "Support social media, customer research, and campaign planning.",
	},
	{
		"title": "IT Support Intern",
		"company": "Island Health Network",
		"island": "Oahu",
		"major": "MIS",
		"season": "Summer",
		"deadline": "March 30, 2026",
		"paid": False,
		"description": "Work with the technology team to support staff and improve systems.",
	},
]

PAGE = """<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Hawaii Internships</title>
	<style>
		/* Simple colors and fonts for the internship website */
		body {
			margin: 0;
			color: #243746;
			background: #f3f7fa;
			font-family: Arial, Helvetica, sans-serif;
		}
		header {
			padding: 18px max(20px, calc((100% - 1000px) / 2));
			color: white;
			background: #173b57;
		}
		.brand { color: white; font-size: 22px; font-weight: bold; text-decoration: none; }
		nav { float: right; }
		nav a { margin-left: 18px; color: white; text-decoration: none; }
		main { width: min(1000px, calc(100% - 32px)); margin: 36px auto; }
		h1, h2, h3 { color: #173b57; }
		.intro { margin-bottom: 24px; }
		.filter-box, .internship-card {
			padding: 20px;
			border: 1px solid #dce5eb;
			border-radius: 10px;
			background: white;
		}
		.filter-box { margin-bottom: 26px; }
		.filters { display: flex; flex-wrap: wrap; gap: 12px; align-items: end; }
		label { display: grid; gap: 5px; font-weight: bold; }
		select { min-width: 150px; padding: 9px; border: 1px solid #bdcbd3; border-radius: 6px; background: white; font: inherit; }
		button, .apply-link {
			display: inline-block;
			padding: 9px 14px;
			border: 0;
			border-radius: 6px;
			color: white;
			background: #167d78;
			font: inherit;
			text-decoration: none;
			cursor: pointer;
		}
		button:hover, .apply-link:hover { background: #116661; }
		.internship-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 16px; }
		.internship-card h3 { margin: 0 0 5px; }
		.company { margin-top: 0; color: #647987; font-weight: bold; }
		.tag { display: inline-block; margin: 3px 4px 8px 0; padding: 3px 9px; border-radius: 20px; color: #173b57; background: #e8f2f5; font-size: 14px; }
		.deadline { font-size: 14px; }
		.empty { color: #647987; }
		footer { padding: 18px; color: #647987; text-align: center; }
		@media (max-width: 600px) {
			header { padding: 16px; }
			nav { float: none; margin-top: 12px; }
			nav a { margin: 0 14px 0 0; }
			main { margin-top: 24px; }
			.filters, .filters label, .filters select { width: 100%; }
		}
	</style>
</head>
<body>
<header>
	<a class="brand" href="/">Hawaii Internships</a>
	<nav><a href="#internships">Browse</a><a href="#saved">Saved</a><a href="#account">Account</a></nav>
</header>
<main>
	<section class="intro">
		<h1>Find an internship in Hawaiʻi</h1>
		<p>Explore opportunities by island, major, and season.</p>
	</section>

	<section class="filter-box">
		<h2>Filter internships</h2>
		<form method="get" class="filters">
			<label>Major
				<select name="major">
					<option value="">All majors</option>
					{% for major in majors %}<option value="{{ major }}" {% if selected_major == major %}selected{% endif %}>{{ major }}</option>{% endfor %}
				</select>
			</label>
			<label>Island
				<select name="island">
					<option value="">All islands</option>
					{% for island in islands %}<option value="{{ island }}" {% if selected_island == island %}selected{% endif %}>{{ island }}</option>{% endfor %}
				</select>
			</label>
			<button type="submit">Search</button>
			<a class="apply-link" href="/">Clear</a>
		</form>
	</section>

	<section id="internships">
		<h2>Internship opportunities ({{ internships|length }})</h2>
		{% if internships %}
		<div class="internship-list">
			{% for internship in internships %}
			<article class="internship-card">
				<h3>{{ internship.title }}</h3>
				<p class="company">{{ internship.company }}</p>
				<span class="tag">{{ internship.island }}</span>
				<span class="tag">{{ internship.major }}</span>
				<span class="tag">{{ internship.season }}</span>
				{% if internship.paid %}<span class="tag">Paid</span>{% endif %}
				<p>{{ internship.description }}</p>
				<p class="deadline">Apply by <strong>{{ internship.deadline }}</strong></p>
				<a class="apply-link" href="#">View opportunity</a>
				<button type="button">Save</button>
			</article>
			{% endfor %}
		</div>
		{% else %}
		<p class="empty">No sample listings match those filters. Try another choice.</p>
		{% endif %}
	</section>
</main>
<footer>Hawaii Internships · Design preview</footer>
</body>
</html>"""


@app.route("/")
def home():
	"""Show the sample page and let visitors try the major/island filters."""
	major = request.args.get("major", "")
	island = request.args.get("island", "")
	internships = [
		item for item in SAMPLE_INTERNSHIPS
		if (not major or item["major"] == major)
		and (not island or item["island"] == island)
	]
	return render_template_string(
		PAGE,
		internships=internships,
		majors=sorted({item["major"] for item in SAMPLE_INTERNSHIPS}),
		islands=sorted({item["island"] for item in SAMPLE_INTERNSHIPS}),
		selected_major=major,
		selected_island=island,
	)


if __name__ == "__main__":
	app.run(debug=True, port=5001)
