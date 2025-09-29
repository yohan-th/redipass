from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# --- CONFIGURATION ---
SERVICE_ACCOUNT_FILE = "data/google-creds.json"  # Chemin vers votre clé JSON
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
DELEGATED_USER = "contact@yotho.pro"  # L'adresse Gmail qui enverra les emails
DESTINATAIRE = "yohan.web@outlook.com"

def send_email(sujet: str, contenu: str):
    # Créer les credentials et déléguer à l'utilisateur Gmail
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    delegated_creds = creds.with_subject(DELEGATED_USER)

    # Construire le service Gmail
    service = build("gmail", "v1", credentials=delegated_creds)

    # Créer le message MIME
    message = MIMEText(contenu)
    message["to"] = DESTINATAIRE
    message["subject"] = sujet

    # Encoder en base64 pour Gmail API
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Envoyer le mail
    sent_message = service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()

# send_email('test', 'test')