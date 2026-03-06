from instagrapi import Client
import os
from dotenv import load_dotenv
import time

# تحميل environment variables
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# admins
allowed_users = [
    "_dq2n",
    "5z_pbi",
    "elin__aax",
    "nvvvsr__",
    "iamforoe",
    "marv_van_matk_2"
]

# روابط ممنوعة
banned_links = ["http", "https", "ig.me"]

# init client
cl = Client()
cl.login(USERNAME, PASSWORD)

checked = set()
messages = {}

print("البوت شغال! مراقبة أي جروب فيه admin من القائمة 24/24 ...")

while True:
    try:
        # fetch threads مع تجاهل media errors
        try:
            threads = cl.direct_threads(amount=20)
        except Exception as e:
            print(f"تجاهل fetch threads بسبب media error: {e}")
            threads = []

        for thread in threads:
            # تحقق واش فيه admin من allowed_users
            participants = [cl.user_info(u).username for u in thread.users]
            if not any(admin in participants for admin in allowed_users):
                continue  # skip الجروبات اللي ما فيهاش admin

            for msg in thread.messages:
                if msg.id in checked:
                    continue
                checked.add(msg.id)

                try:
                    text = (msg.text or "").lower()
                    user = cl.user_info(msg.user_id).username

                    # ignore media: if text is empty skip (Reels, images, voice)
                    if not text:
                        continue

                    # spam detection
                    if user not in messages:
                        messages[user] = []
                    messages[user].append(text)
                    spam = messages[user].count(text) >= 3

                    # link detection
                    link_detected = any(link in text for link in banned_links)

                    if (spam or link_detected) and user not in allowed_users:
                        cl.direct_send(
                            f"Tam tard zaml bok ⛔️",
                            thread_ids=[thread.id]
                        )
                        cl.direct_thread_remove_user(thread.id, msg.user_id)

                except Exception as e:
                    print(f"تجاهل رسالة بسبب media error: {e}")
                    continue

    except Exception as main_e:
        print(f"خطأ رئيسي آخر: {main_e}")

    time.sleep(8)
