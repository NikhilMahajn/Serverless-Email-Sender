from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)


@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.get_json() 
    if not data:
        return jsonify({"error": "Invalid JSON request"}), 400

    receiver_email = data.get("receiver_email")
    subject = data.get("subject")
    body_text = data.get("body_text")

    if not receiver_email or not subject or not body_text:
        return jsonify({"error": "Missing required fields"}), 400

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")  
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        return jsonify({"error": "SMTP credentials are missing"}), 500

    SENDER_EMAIL = smtp_user
    try:
        msg = MIMEText(body_text)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receiver_email, msg.as_string())

        return jsonify({"message": "Email sent successfully"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
