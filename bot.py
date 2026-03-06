from instagrapi import Client
import os
from dotenv import load_dotenv
import time

# تحميل المتغيرات من .env local أو Environment Variables في Railway
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# الحسابات admins / المسموح لهم
allowed_users = [
    "_dq2n",
    "5z_pbi",
    "elin__aax",
    "nvvvsr__",
    "iamforoe",
    "marv_van_matk_2"  # admin جديد
]

# IDs ديال الجروبات اللي البوت يراقبهم فقط
allowed_threads = [
    1234567890,  # حط هنا ID ديال الجروب الأول
    9876543210   # ID ديال الجروب الثاني إذا كاين
]

# ربط الحساب بالبوت
cl = Client()
cl.login(USERNAME, PASSWORD)

# لتجنب معالجة نفس الرسالة أكثر من مرة
checked = set()
messages = {}

# روابط ممنوعة
banned_links = [
    "http",
    "www",
    ".com",
    ".net",
    "ig.me",
    "instagram.com",
    "t.me",
    "discord.gg",
    "bit.ly"
]

print("البوت شغال! مراقبة الجروبات المحددة 24/24 ...")

while True:
    threads = cl.direct_threads(amount=10)
    for thread in threads:

        # فقط الجروبات اللي اخترنا
        if thread.id not in allowed_threads:
            continue

        for msg in thread.messages:

            if msg.id in checked:
                continue
            checked.add(msg.id)

            text = (msg.text or "").lower()
            user = cl.user_info(msg.user_id).username

            # كشف spam (نفس الرسالة كتكرر ≥3)
            if user not in messages:
                messages[user] = []
            messages[user].append(text)
            spam = messages[user].count(text) >= 3

            # كشف روابط ممنوعة
            link_detected = any(link in text for link in banned_links)

            # إذا spam أو link وماشي allowed_users
            if (spam or link_detected) and user not in allowed_users:
                cl.direct_send(
                    f"🚫 @{user} تم طردك بسبب السبام أو إرسال رابط ممنوع",
                    thread_ids=[thread.id]
                )
                cl.direct_thread_remove_user(thread.id, msg.user_id)

    time.sleep(8)
