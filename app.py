from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import random


# =========================================================
# SETUP
# =========================================================

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

client = Groq(api_key=api_key)


# =========================================================
# AI PERSONALITIES
# =========================================================

PERSONALITIES = {

    "funny": """
    Make the excuse genuinely funny and clever.
    It should sound like someone desperately trying to justify
    something silly while still being somewhat believable.
    Use unexpected logic and playful wording.
    """,

    "dramatic": """
    Make the excuse extremely dramatic.
    Treat a completely normal situation like a major life event.
    Make it emotional, theatrical and unnecessarily serious.
    """,

    "smart": """
    Make the excuse sound intelligent and technically convincing.
    Use sophisticated but understandable reasoning.
    It should sound like someone is trying very hard to make
    procrastination sound scientifically justified.
    """,

    "ridiculous": """
    Make the excuse completely absurd and chaotic.
    Use bizarre logic, strange coincidences and unexpected ideas.
    It should make absolutely no sense but still be funny.
    """
}


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# GENERATE AI EXCUSE
# =========================================================

@app.route("/generate", methods=["POST"])
def generate_excuse():

    data = request.get_json()

    activity = data.get("activity", "").strip()
    style = data.get("style", "funny")

    if not activity:
        return jsonify({
            "success": False,
            "message": "Tell me what you're doing first 😭"
        })

    if style not in PERSONALITIES:
        style = "funny"


    personality = PERSONALITIES[style]


    # =====================================================
    # PROMPT
    # =====================================================

    prompt = f"""
You are EXCUSE.exe, a useless but extremely creative excuse generator.

The user is supposed to be doing:
"{activity}"

Personality:
{personality}

Generate ONE completely original excuse.

Rules:
- Do NOT reuse common cliché excuses.
- Do NOT use a fixed template.
- Make every response feel different.
- Keep it short: 1 or 2 sentences.
- Directly relate the excuse to the user's activity.
- Do not explain the joke.
- Do not put quotation marks around the answer.
- Make it entertaining and suitable for a fun college hackathon project.
- Do not generate excuses involving dangerous, illegal or harmful actions.

Return ONLY the excuse.
"""


    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are EXCUSE.exe. "
                        "You create short, original, funny excuses."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=1.15,
            max_tokens=100
        )


        excuse = response.choices[0].message.content.strip()


        # =================================================
        # FUN FAKE STATS
        # =================================================

        if style == "funny":
            believability = random.randint(40, 70)
            ridiculousness = random.randint(65, 90)

        elif style == "dramatic":
            believability = random.randint(35, 65)
            ridiculousness = random.randint(70, 95)

        elif style == "smart":
            believability = random.randint(65, 90)
            ridiculousness = random.randint(25, 55)

        else:
            believability = random.randint(5, 35)
            ridiculousness = random.randint(90, 100)


        caught = 100 - believability


        return jsonify({

            "success": True,

            "excuse": excuse,

            "believability": believability,

            "ridiculousness": ridiculousness,

            "caught": caught

        })


    except Exception as error:

        print("GROQ ERROR:", error)

        return jsonify({

            "success": False,

            "message":
                "EXCUSE.exe couldn't contact its AI brain 💀"

        })


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)