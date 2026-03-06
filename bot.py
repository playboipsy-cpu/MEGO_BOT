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

# روابط ممنوعة (أي link)
banned_links = ["http", "https", "ig.me"]

# init client
cl = Client()
cl.login(USERNAME, PASSWORD)

checked = set()
messages = {}

print("البوت شغال! مراقبة أي جروب فيه admin من القائمة 24/24 ...")

while True:
    try:
        # جلب آخر threads مع تجاهل أي media error
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

                    # ---------- !ping command ----------
                    if text.strip() == "!ping":
                        cl.direct_send(
                            "pong",
                            thread_ids=[thread.id]
                        )
                        continue  # ما ندخلوش في باقي checks للرسالة نفسها

                    # استخراج أي link من preview أو text
                    preview_links = []
                    if getattr(msg, "link", None):
                        preview_links.append(msg.link)
                    if getattr(msg, "mentioned_media", None):
                        for m in msg.mentioned_media:
                            if hasattr(m, "url"):
                                preview_links.append(m.url)

                    # link detection: سواء ف text أو preview_links
                    link_detected = any(link in text for link in banned_links) or any(
                        any(bl in pl.lower() for bl in banned_links) for pl in preview_links
                    )

                    # ignore media: إذا ماكانش text وماكانش link
                    if not text and not preview_links:
                        continue

                    # spam detection
                    if user not in messages:
                        messages[user] = []
                    if text:
                        messages[user].append(text)
                    spam = any(messages[user].count(t) >= 3 for t in messages[user])

                    # kick أي user غير admin إذا spam أو link
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
