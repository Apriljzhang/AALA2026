import os
import smtplib
import socket
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf"}
MAX_FILE_BYTES = 8 * 1024 * 1024

SMTP_HOST = os.getenv("SMTP_HOST", "smtp-mail.outlook.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USERNAME)
MAILBOX_TO = os.getenv("MAILBOX_TO", "aala2026@outlook.com")


def _validate_email_field(value: str, label: str):
    if not value or "@" not in value:
        raise ValueError(f"{label} is invalid.")


def _validate_and_read_file(file_storage, label: str):
    if not file_storage or not file_storage.filename:
        raise ValueError(f"{label} is required.")

    safe_name = secure_filename(file_storage.filename)
    suffix = Path(safe_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"{label} must be PNG, JPG, WEBP, or PDF.")

    payload = file_storage.read()
    if len(payload) == 0:
        raise ValueError(f"{label} cannot be empty.")
    if len(payload) > MAX_FILE_BYTES:
        raise ValueError(f"{label} must be 8MB or smaller.")

    mime = file_storage.mimetype or "application/octet-stream"
    return {
        "filename": safe_name,
        "mime": mime,
        "payload": payload,
    }


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(_error):
    return jsonify({"error": "Total upload size exceeds 20MB."}), 413


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/api/send-registration-email", methods=["POST", "OPTIONS"])
def send_registration_email():
    if request.method == "OPTIONS":
        return ("", 204)

    participant_email = request.form.get("participantEmail", "").strip()
    subject = request.form.get("subject", "").strip()
    content = request.form.get("content", "").strip()
    submission_id = request.form.get("submissionId", "").strip()
    role = request.form.get("role", "").strip().lower()
    is_macau_local = request.form.get("isMacauLocal", "false").strip().lower() == "true"

    try:
        _validate_email_field(participant_email, "Participant email")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not subject:
        return jsonify({"error": "Email subject is required."}), 400
    if not content:
        return jsonify({"error": "Email content is required."}), 400
    if len(subject) > 200:
        return jsonify({"error": "Email subject is too long."}), 400
    if len(content) > 20000:
        return jsonify({"error": "Email content is too long."}), 400
    if role in {"presenter", "student"} and submission_id.upper() == "AALA2026":
        return jsonify({"error": "Submission ID cannot be only AALA2026. Please append three or four digits."}), 400

    payment_proof_file = request.files.get("paymentProofFile")
    id_doc_file = request.files.get("idDocumentationFile")
    id_document_required = role == "student" or is_macau_local

    try:
        payment_proof = _validate_and_read_file(payment_proof_file, "Payment proof file")
        id_document = None
        if id_doc_file and id_doc_file.filename:
            id_document = _validate_and_read_file(id_doc_file, "ID documentation file")
        if id_document_required and not id_document:
            raise ValueError("ID documentation file is required for student or Macau local registration.")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if not SMTP_USERNAME or not SMTP_PASSWORD or not SMTP_FROM:
        return jsonify({"error": "SMTP credentials are not configured on the server."}), 500

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = SMTP_FROM
    message["To"] = MAILBOX_TO
    message["Reply-To"] = participant_email
    message.set_content(content)

    payment_main, payment_sub = payment_proof["mime"].split("/", 1) if "/" in payment_proof["mime"] else ("application", "octet-stream")
    message.add_attachment(
        payment_proof["payload"],
        maintype=payment_main,
        subtype=payment_sub,
        filename=payment_proof["filename"],
    )

    if id_document:
        id_main, id_sub = id_document["mime"].split("/", 1) if "/" in id_document["mime"] else ("application", "octet-stream")
        message.add_attachment(
            id_document["payload"],
            maintype=id_main,
            subtype=id_sub,
            filename=id_document["filename"],
        )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(message)
    except smtplib.SMTPAuthenticationError:
        return jsonify({
            "error": "SMTP authentication failed. Check SMTP_USERNAME/SMTP_PASSWORD and use an Outlook app password if required."
        }), 502
    except smtplib.SMTPConnectError:
        return jsonify({
            "error": f"Cannot connect to SMTP server at {SMTP_HOST}:{SMTP_PORT}."
        }), 502
    except smtplib.SMTPServerDisconnected:
        return jsonify({
            "error": "SMTP server disconnected unexpectedly. Please try again."
        }), 502
    except socket.timeout:
        return jsonify({
            "error": f"SMTP connection timed out for {SMTP_HOST}:{SMTP_PORT}."
        }), 502
    except OSError as exc:
        return jsonify({
            "error": f"Network error while contacting SMTP server: {exc.__class__.__name__}."
        }), 502
    except smtplib.SMTPException as exc:
        return jsonify({
            "error": f"SMTP error while sending email: {exc.__class__.__name__}."
        }), 502
    except Exception:
        return jsonify({"error": "Failed to send registration email. Please try again later."}), 502

    return jsonify({"ok": True})


@app.get("/api/health")
def health():
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8787, debug=True)
