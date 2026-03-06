import os
import time
from instagrapi import Client

# ----------------------------
# Login credentials
# ----------------------------
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(USERNAME, PASSWORD)
print("البوت شغال! مراقبة أي جروب يدخل فيه 24/24 ...")

# ----------------------------
# Message & cooldown
# ----------------------------
MESSAGE = """╔═════════⚠️═════════╗
ْ  𝐖𝐄𝐈𝐑𝐃 𝐖𝐎𝐑𝐋𝐃 𝐅𝐎𝐔𝐍𝐃𝐀𝐓𝐈𝐎𝐍 
╚═════════👁═════════╝

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

╔━━━━━━━━⊱⭐️⊰━━━━━━━━╗

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝐃
📛_____________𝑻9𝑨𝑩𝑨_______________📛

https://ig.me/j/AbardcPA57d-g4Rb/
"""

cooldown = 20  # ← هاد الرقم هو اللي كتحكم فيه فالوقت بين كل رسالة

spamming = {}  # لكل thread الحالة ديالو (True/False)

# ----------------------------
# Main loop
# ----------------------------
while True:
    try:
        threads = cl.direct_threads(amount=20)  # آخر 20 thread
        for thread in threads:
            thread_id = thread.id

            # إنشاء الحالة لكل thread إلا ماكانش
            if thread_id not in spamming:
                spamming[thread_id] = False

            # جلب آخر 5 ميساجات
            messages = cl.direct_messages(thread_id, amount=5)
            for msg in messages:
                if msg.text is None:
                    continue

                text = msg.text.lower()

                # أوامر start / stop
                if text == "start":
                    spamming[thread_id] = True
                    cl.direct_send("Spam started.", thread_ids=[thread_id])

                if text == "stop":
                    spamming[thread_id] = False
                    cl.direct_send("Spam stopped.", thread_ids=[thread_id])

            # إرسال الرسالة إذا thread مفعل
            if spamming[thread_id]:
                cl.direct_send(MESSAGE, thread_ids=[thread_id])
                time.sleep(cooldown)

    except Exception as e:
        print("خطأ رئيسي ف fetch threads:", e)
        time.sleep(10)
