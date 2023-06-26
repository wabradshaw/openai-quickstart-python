import os

import openai
from flask import Flask, redirect, render_template, request, url_for

JOKE_SYSTEM = """You are a comedian that tells jokes in the following format:

<A, B, C, D, E>
S
E!

Where each symbol has the following meaning:
A -> A random word or phrase of at least 8 letters.
B -> The word that A either starts or ends with. 
C -> A random word that either sounds like B or rhymes with B. The length of B and C should either be the same, or differ by 1 character.
D -> A new word made by substituting C for D in A.
S -> The setup. It should describe a combination of A and C.

Here are some examples:

<nightmare, night, fight, fightmare>
What do you call a cross between a bad dream and a battle?
A fightmare!

<Cupcake, cup, pup, pupcake>
What dog is made in a bakery?
A pupcake!

<Guitar, tar, star, guistar>
What do you call a musical instrument that shines like a celestial body?
A guistar!

<Wonderful, won, run, runderful>
What do you call an amazing race?
Runderful!"""

GENERIC_JOKE_PROMPT = "Tell a joke"

MODEL = "gpt-3.5-turbo"

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        response = openai.ChatCompletion.create(            
            model=MODEL,
            messages=[
                {"role": "system", "content": JOKE_SYSTEM},
                {"role": "user", "content": GENERIC_JOKE_PROMPT}
            ],            
            temperature=1.5
        )
        joke = response.choices[0].message.content
        return redirect(url_for("index", result=joke))

    result = request.args.get("result")
    return render_template("index.html", result=result)



