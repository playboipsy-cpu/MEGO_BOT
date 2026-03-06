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
print("البوت شغال! غادي يسيفط الرسائل فقط فالـ groups ...")

# ----------------------------
# الرسالة اللي بغيت يسيفط
# ----------------------------
MESSAGE = """╔═════════⚠️═════════╗
ْ  𝐖𝐄𝐈𝐑𝐃 𝐖𝐎𝐑𝐋𝐃 𝐅𝐎𝐔𝐍𝐃𝐀𝐓𝐈𝐎𝐍 
╚═════════👁═════════╝

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

╔━━━━━━━━⊱⭐️⊰━━━━━━━━╗

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝐑𝐃_______________________𝑾𝑶𝐑𝐋𝐃
📛_____________𝑻9𝑨𝑩𝐀_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

https://ig.me/j/AbardcPA57d-g4Rb/
"""

# ----------------------------
# Cooldown بالثواني بين كل رسالة
# ----------------------------
COOLDOWN = 20

# ----------------------------
# Dictionary باش نخلي كل group يقدر يبدأ ويوقف رسائله
# ----------------------------
active_groups = {}  # key = thread.id, value = True/False

# ----------------------------
# Loop الأساسي
# ----------------------------
while True:
    try:
        threads = cl.direct_threads(amount=50)  # جلب آخر 50 thread
        for thread in threads:
            # فقط groups
            if thread.type != "group":
                continue
            
            last_message = thread.messages[0].text if thread.messages else ""
            last_message_lower = last_message.lower() if last_message else ""

            # !start → يفعل الإرسال فهاد group
            if "!start" in last_message_lower:
                active_groups[thread.id] = True
                cl.direct_send("✅ البوت بدا يسيفط فالـ group!", thread_ids=[thread.id])
                continue

            # !stop → يوقف الإرسال فهاد group
            if "!stop" in last_message_lower:
                active_groups[thread.id] = False
                cl.direct_send("⛔️ البوت وقف فالـ group!", thread_ids=[thread.id])
                continue

            # إذا group مفعل
            if active_groups.get(thread.id):
                cl.direct_send(MESSAGE, thread_ids=[thread.id])
                print(f"تم إرسال الرسالة ل group {thread.id}")
                time.sleep(COOLDOWN)

    except Exception as e:
        print(f"خطأ: {e}")
        time.sleep(5)
