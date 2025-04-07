from fastapi import FastAPI, Form
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()  # تحميل متغيرات البيئة من ملف .env

app = FastAPI()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

@app.get("/")
async def read_root():
    return {"message": "HR Hub Backend is running 🎉"}

@app.post("/send-email")
async def send_email(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    msg = EmailMessage()
    msg['Subject'] = f'HR Hub Contact - رسالة من {name}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(f"""
    اسم المُرسل: {name}
    البريد الإلكتروني: {email}
    
    الرسالة:
    {message}
    """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("hrhub.sa@gmail.com", "zcpp rech ivdg qblv")
            smtp.send_message(msg)
        return {"message": "تم الإرسال بنجاح ✅"}
    except Exception as e:
        return {"error": f"فشل في الإرسال: {str(e)}"}
