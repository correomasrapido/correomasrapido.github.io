import os
import re
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Flask
app = Flask(__name__)

# Configuración del correo
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = 587  # Puede cambiar según el servidor de correo
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Expresión regular para validar correos electrónicos
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        # Obtener los datos del formulario
        emails = request.form['emails'].split(',')
        subject = request.form['subject'].strip()
        message = request.form['message'].strip()

        # Validación de correos electrónicos
        valid_emails = []
        for email in emails:
            email = email.strip()
            if re.match(EMAIL_REGEX, email):
                valid_emails.append(email)

        if not valid_emails:
            return jsonify({"status": "error", "message": "Debe ingresar al menos un correo válido"}), 400

        # Verificar que el asunto y mensaje no estén vacíos
        if not subject or not message:
            return jsonify({"status": "error", "message": "Asunto y mensaje son obligatorios"}), 400

        # Crear el mensaje para el correo
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL

        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            for email in valid_emails:
                msg['To'] = email
                server.sendmail(SENDER_EMAIL, email, msg.as_string())

        return jsonify({"status": "success", "message": "Correos enviados exitosamente"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
