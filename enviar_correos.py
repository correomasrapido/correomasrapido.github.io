from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import smtplib
from email.mime.text import MIMEText
import re
import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración del límite de peticiones
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]  # Máximo 10 peticiones por minuto
)

# Configuración del servidor SMTP y credenciales
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# Expresión regular para validar correos electrónicos
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def validate_email_list(email_list):
    """Valida una lista de correos electrónicos y retorna los válidos."""
    return [email.strip() for email in email_list if re.match(EMAIL_REGEX, email.strip())]

def verify_recaptcha(recaptcha_response):
    """Verifica la respuesta de reCAPTCHA con la API de Google."""
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}
    )
    result = response.json()
    return result.get('success', False)

@app.route('/send-email', methods=['POST'])
@limiter.limit("5 per minute")  # Limitar esta ruta a 5 peticiones por minuto
def send_email():
    try:
        # Validar datos del formulario
        emails = request.form.get('emails', '').split(',')
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        recaptcha_response = request.form.get('g-recaptcha-response')

        if not subject or not message:
            return jsonify({"status": "error", "message": "El asunto y el mensaje son obligatorios"}), 400

        if not recaptcha_response or not verify_recaptcha(recaptcha_response):
            return jsonify({"status": "error", "message": "reCAPTCHA no validado o inválido"}), 400

        valid_emails = validate_email_list(emails)
        if not valid_emails:
            return jsonify({"status": "error", "message": "Debe ingresar al menos un correo válido"}), 400

        if len(message) > 5000:
            return jsonify({"status": "error", "message": "El mensaje es demasiado largo"}), 400

        # Configuración del mensaje de correo
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL

        # Enviar correos electrónicos de forma segura
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            for email in valid_emails:
                msg['To'] = email
                try:
                    server.sendmail(SENDER_EMAIL, email, msg.as_string())
                except smtplib.SMTPException as e:
                    app.logger.error(f"Error enviando correo a {email}: {e}")
                    continue

        return jsonify({"status": "success", "message": "Correos enviados exitosamente"}), 200

    except smtplib.SMTPException as e:
        app.logger.error(f"Error con el servidor SMTP: {e}")
        return jsonify({"status": "error", "message": "Error al enviar correos electrónicos"}), 500
    except Exception as e:
        app.logger.error(f"Error inesperado: {e}")
        return jsonify({"status": "error", "message": "Ha ocurrido un error inesperado"}), 500

if __name__ == '__main__':
    app.run(debug=True)
