# Registration Email Backend (Outlook SMTP)

This backend provides a single API endpoint:

- `POST /api/send-registration-email`

It is designed to receive multipart form data from `registration.html` and send an email with attachments to `aala2026@outlook.com` using Outlook SMTP.

## 1) Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Environment Variables

Set the following variables before running:

- `SMTP_HOST` (default: `smtp-mail.outlook.com`)
- `SMTP_PORT` (default: `587`)
- `SMTP_USERNAME` (required)
- `SMTP_PASSWORD` (required)
- `SMTP_FROM` (optional, defaults to `SMTP_USERNAME`)
- `MAILBOX_TO` (optional, defaults to `aala2026@outlook.com`)

## 3) Run

```bash
python app.py
```

The server listens on port `8787` by default.

## 4) Payload Expectations

Form fields:

- `participantEmail` (required)
- `subject` (required)
- `content` (required)

File fields:

- `paymentProofFile` (required)
- `idDocumentationFile` (optional)

Accepted file extensions: `.png`, `.jpg`, `.jpeg`, `.webp`, `.pdf`
Max file size per attachment: `8MB`
Total request limit: `20MB`
