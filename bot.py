from instagrapi import Client
import os
from dotenv import load_dotenv
import time

# تحميل المتغيرات من .env local أو Environment Variables في Railway
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# حسابات admins أو المستخدمين المسموح لهم
allowed_users = [
    "admin1",
    "admin2",
    "friend1"
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

print("البوت شغال! مراقبة الجروب 24/24 ...")

while True:
    threads = cl.direct_threads(amount=10)

    for thread in threads:
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