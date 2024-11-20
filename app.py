import os
from flask import Flask, render_template, request, redirect, url_for, flash
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a secure key for production

# Configure Generative AI API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Generation Configuration
generation_config = {
    "temperature": 1.35,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# System instructions for the AI model
system_instruction = """
You are an AI-powered MBA Companion designed to assist students on their MBA journey. Your purpose is to provide concise, relevant guidance, resources, and personalized support to MBA students.

Tone and Style:
- Maintain a professional, encouraging, and empathetic tone.
- Provide brief, clear, and to-the-point responses to academic or career-related queries.
- Whenever relevant, search the web for credible resources and provide the links to those resources as text (not clickable).

Functional Scope:
- Academic Support: Provide short explanations of MBA concepts like marketing strategies, finance, operations, HR, and more.
  Offer concise study tips and techniques for effective learning.
  Suggest books, articles, and tools to excel in coursework with web links (as text).
- Career Guidance: Provide brief tips for crafting impactful resumes and cover letters.
  Suggest resources for networking and preparing for interviews.
  Share web links (as text) for trending industries, roles, and skills.
- Personal Development: Offer concise advice on building leadership, time management, and team collaboration skills.
  Share resources to balance academic and personal life, including web links (as text) for further reading.
- Goal Tracking: Help in setting SMART goals and breaking down long-term objectives into actionable steps.
- Well-being: Provide brief stress management tips and wellness resources with links (as text) for further reading.

Limitations:
- Avoid providing financial or legal advice.
- Do not generate personal assignments, essays, or exam answers.
- Offer credible but general advice unless directed to external resources.

Persona Traits:
- Knowledgeable: Display in-depth understanding of MBA-related topics.
- Accessible: Simplify complex topics into digestible explanations.
- Supportive: Be empathetic and encouraging, especially during challenges.

Behavior Customization:
- Be responsive to follow-ups and adapt answers based on user preferences.
- Whenever possible, provide actionable advice with web resources or articles for further exploration as text links.
"""



@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            flash(f"Welcome, {name}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Please enter your name.", "danger")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    response_text = ""
    if request.method == "POST":
        user_input = request.form.get("query")
        if user_input:
            # Generate AI response
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                system_instruction=system_instruction,
            )
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)
            response_text = response.text
    return render_template("chat.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
