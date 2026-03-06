from instagrapi import Client
import time

# ⚠️ غيّر هادشي ب username/password ديالك
IG_USERNAME = "YOUR_IG_USERNAME"
IG_PASSWORD = "YOUR_IG_PASSWORD"

# cooldown بالثواني
COOLDOWN = 20

# الرسالة اللي غادي يسيفط البوت
MESSAGE = """
╔═════════⚠️═════════╗
ْ  𝐖𝐄𝐈𝐑𝐃 𝐖𝐎𝐑𝐋𝐃 𝐅𝐎𝐔𝐍𝐃𝐀𝐓𝐈𝐎𝐍 
╚═════════👁═════════╝

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝑫
📛_____________𝑻9𝑨𝑩𝑨_______________📛

╔━━━━━━━━⊱⭐️⊰━━━━━━━━╗

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝑫
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝑫
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝑫
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝑫
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝑫
📛_____________𝑻9𝑨𝑩𝑨_______________📛

━━━━━━━━━⊱⭐️⊰━━━━━━━━━

https://ig.me/j/AbardcPA57d-g4Rb/
"""

# قائمة باش نخزنو state لكل group
active_groups = {}

# تسجيل الدخول
cl = Client()
cl.login(IG_USERNAME, IG_PASSWORD)
print("✅ البوت شغال! مراقبة أي group 24/24 ...")

# loop باش يتشيك الرسائل
while True:
    try:
        threads = cl.direct_threads(amount=50)
        for thread in threads:
            if thread.type != "group":
                continue  # غي group فقط

            last_message = thread.messages[0].text if thread.messages else None
            if not last_message:
                continue  # نتجاهل أي media / reels / صوت

            last_message_lower = last_message.lower()

            # start command
            if "!start" in last_message_lower:
                active_groups[thread.id] = True
                try:
                    cl.direct_send("✅ البوت بدا يسيفط فالـ group!", thread_ids=[thread.id])
                except:
                    pass
                continue

            # stop command
            if "!stop" in last_message_lower:
                active_groups[thread.id] = False
                try:
                    cl.direct_send("⛔️ البوت وقف فالـ group!", thread_ids=[thread.id])
                except:
                    pass
                continue

            # إرسال الرسائل تلقائيًا
            if active_groups.get(thread.id):
                try:
                    cl.direct_send(MESSAGE, thread_ids=[thread.id])
                    print(f"تم إرسال الرسالة ل group {thread.id}")
                    time.sleep(COOLDOWN)
                except Exception as e:
                    print(f"خطأ فـ إرسال الرسالة: {e}")
                    continue  # أي media error → نتجاهلو
    except Exception as e:
        print(f"خطأ فالـ loop: {e}")
        time.sleep(5)
