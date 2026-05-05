from flask import Flask, request, render_template, redirect
from services.db import init_db, save_user, mark_paid, get_user
from services.storage import upload_file
from services.payments import create_checkout
from services.ai import extract_text, analyze_contract
from services.emailer import send_email
import stripe, os

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    user_id = request.form["user_id"]

    url = upload_file(file)
    save_user(user_id, url)

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/checkout", methods=["POST"])
def checkout():
    user_id = request.form["user_id"]
    tier = request.form["tier"]

    url = create_checkout(user_id, tier)
    return redirect(url)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig = request.headers.get("Stripe-Signature")

    event = stripe.Webhook.construct_event(
        payload, sig, os.getenv("STRIPE_WEBHOOK_SECRET")
    )

    if event["type"] == "checkout.session.completed":
        user_id = event["data"]["object"]["metadata"]["user_id"]
        mark_paid(user_id)

    return "ok"

@app.route("/analyze", methods=["POST"])
def analyze():
    user_id = request.form["user_id"]
    email = request.form["email"]

    user = get_user(user_id)

    if not user or not user[2]:
        return "Payment required"

    file_url = user[1]

    text = extract_text(file_url)
    result = analyze_contract(text)

    send_email(email, result)

    return render_template("result.html", result=result)
