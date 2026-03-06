import os
import time
from instagrapi import Client

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(USERNAME, PASSWORD)

print("Bot started...")

cooldown = 5
spamming = {}

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

𝑾𝑬𝑰𝑹𝑫_______________________𝑾𝑶𝑹𝑳𝑫
📛_____________𝑻9𝑨𝑩𝑨_______________📛

https://ig.me/j/AbardcPA57d-g4Rb/
"""

while True:
    try:
        threads = cl.direct_threads(amount=20)

        for thread in threads:

            thread_id = thread.id

            if thread_id not in spamming:
                spamming[thread_id] = False

            messages = cl.direct_messages(thread_id, amount=5)

            for msg in messages:

                if msg.text is None:
                    continue

                text = msg.text.lower()

                if text == "start":
                    spamming[thread_id] = True
                    cl.direct_send("Spam started.", thread_ids=[thread_id])

                if text == "stop":
                    spamming[thread_id] = False
                    cl.direct_send("Spam stopped.", thread_ids=[thread_id])

            if spamming[thread_id]:
                cl.direct_send(MESSAGE, thread_ids=[thread_id])
                time.sleep(cooldown)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
