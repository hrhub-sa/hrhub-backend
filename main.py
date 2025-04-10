from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()  # تحميل متغيرات البيئة من ملف .env

app = FastAPI()

# حل لمشكلة CORS لو أرسلت من موقع آخر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hrhub-sa.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

@app.get("/")
async def read_root():
    return {"message": "HR Hub Backend is running 🎉"}

@app.post("/send-email")
async def send_email(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...),
    attachment: UploadFile = File(None)  # يقبل الملف كاختياري
):
    msg = EmailMessage()
    msg['Subject'] = f'HR Hub Contact - رسالة من {name}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(f"""
    اسم المُرسل: {name}
    البريد الإلكتروني: {email}
    رقم الهاتف: {phone}

    الرسالة:
    {message}
    """)

    # إضافة المرفق إذا تم رفعه
    if attachment:
        file_data = attachment.file.read()
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=attachment.filename)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return {"message": "تم الإرسال بنجاح ✅"}
    except Exception as e:
        return {"error": f"فشل في الإرسال: {str(e)}"}
