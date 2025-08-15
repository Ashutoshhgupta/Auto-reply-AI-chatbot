import pyautogui
import pyperclip
import time
from openai import OpenAI
from tone_responder import ask_deepseek_with_tone

# --- DeepSeek client setup ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    default_headers={
        "Authorization": "Bearer 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",
        "HTTP-Referer": "https://yourapp.com"
    }
)

# --- Step 1: GUI to copy chat ---
print("⚠️ Script starting in 3 seconds... Switch to your target app/window!")
time.sleep(3)

pyautogui.click(972, 851)  # focus chat
time.sleep(1)

pyautogui.moveTo(508, 168, duration=0.5)
pyautogui.mouseDown(button='left')
pyautogui.moveTo(986, 816, duration=2.0)
pyautogui.mouseUp(button='left')
time.sleep(1)

pyautogui.hotkey('command', 'c')  # ⌘+C (macOS) — use 'ctrl' for Windows
time.sleep(1)

chat_clipboard = pyperclip.paste()

# --- Step 2: Append to chat.txt ---
if chat_clipboard.strip():
    with open("chat.txt", "a", encoding="utf-8") as f:
        f.write("\n" + chat_clipboard.strip() + "\n")
else:
    print("❌ Clipboard was empty. Nothing to append.")
    exit()

# --- Step 3: Extract latest G messages ---
def extract_gs_recent_messages(chat_text):
    lines = chat_text.strip().splitlines()
    last_ashutosh_index = -1

    for i in reversed(range(len(lines))):
        if "] Ashutosh:" in lines[i]:
            last_ashutosh_index = i
            break

    g_messages = []
    for line in lines[last_ashutosh_index+1:]:
        if "] G:" in line:
            message_part = line.split("] G:", 1)[1].strip()
            if message_part:
                g_messages.append(message_part)

    return "\n".join(g_messages).strip()

with open("chat.txt", "r", encoding="utf-8") as f:
    chat_history = f.read()

g_recent = extract_gs_recent_messages(chat_history)

if not g_recent:
    print("❌ No valid message from G to respond to.")
    exit()

# --- Step 4: Get DeepSeek reply ---
ask_deepseek_with_tone(g_recent, client)

# --- Step 5: Send reply automatically ---
def get_last_reply():
    try:
        with open("love_diary.txt", "r", encoding="utf-8") as f:
            entries = f.read().strip().split("\n---\n")
            return entries[-1].strip() if entries else None
    except FileNotFoundError:
        print("❌ love_diary.txt not found.")
        return None

final_reply = get_last_reply()

if final_reply:
    pyperclip.copy(final_reply)
    print("✅ Copied reply to clipboard.")

    time.sleep(2)  # Wait before pasting

    pyautogui.click(769, 867)  # click message input box
    time.sleep(0.5)
    pyautogui.hotkey('command', 'v')  # ⌘+V — use 'ctrl' for Windows
    time.sleep(0.3)
    pyautogui.press('enter')  # send
    print("📤 Message sent!")
else:
    print("❌ No response found to send.")
