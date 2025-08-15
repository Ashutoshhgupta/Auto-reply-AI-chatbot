def detect_tone(chat_text):
    lower_chat = chat_text.lower()

    if any(word in lower_chat for word in ["naraz", "gussa", "angry", "upset",'nrz','baat matt kro','katti']):
        return "angry"
    elif any(word in lower_chat for word in ["miss", "love", "baby", "jaan", "❤️", "pyaar", "sweet", "cute",'aashi']):
        return "loving"
    elif any(word in lower_chat for word in ["sad", "cry", "😢", "tension", "sorry", "hurt"]):
        return "sad"
    elif any(word in lower_chat for word in ["happy", "awesome", "good", "great", "😂", "hehe", "hahaha",'lol']):
        return "happy"
    elif any(word in lower_chat for word in ["tension", "worried", "problem", "dhar", "fear",'dikkat','mushkil']):
        return "worried"
    else:
        return "neutral"


def ask_deepseek_with_tone(command, client):
    if not command or not command.strip():
        print("\n⚠️ No valid message to send to DeepSeek.")
        return

    detected_tone = detect_tone(command)
    print(f"\n🧠 Detected Chat Tone: {detected_tone}")

    base_prompt = (
        "You are Ashutosh, a loving, caring person from Jammu, who speaks Hindi and English casually "
        "(Hinglish style). You are chatting naturally on WhatsApp with your close one."
    )

    if detected_tone == "happy":
        tone_instruction = "Reply playfully and lovingly using Hindi and English mixed sentences."
    elif detected_tone == "sad":
        tone_instruction = "Reply emotionally, softly, and lovingly using Hindi and English mixed sentences to console them."
    elif detected_tone == "angry":
        tone_instruction = "Reply calmly, reassuringly, and lovingly using Hindi and English mixed sentences to calm them down."
    elif detected_tone == "worried":
        tone_instruction = "Reply supportively and lovingly using Hindi and English mixed sentences to remove their tension."
    elif detected_tone == "loving":
        tone_instruction = "Reply very romantically and cutely using Hindi and English mixed sentences."
    else:
        tone_instruction = "Reply naturally and casually using Hindi and English mixed sentences."

    system_prompt = f"{base_prompt} {tone_instruction}"

    #print("\n🧪 System Prompt Sent:\n", system_prompt)
    #print("\n📝 Message Sent to DeepSeek:\n", command)

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-zero:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            stream=False
        )

        message = response.choices[0].message.content if response.choices else None
        final_text = message.strip() if message else None

        if final_text:
            #print("\n✅ Final Reply (Hinglish + Tone Detected):\n")
            print(final_text)

            # Optional: save reply to diary
            with open("love_diary.txt", "a", encoding="utf-8") as f:
                f.write("\n---\n" + final_text + "\n")
        else:
            print("\n❌ DeepSeek returned empty. Try again.")

    except Exception as e:
        print(f"\n❌ DeepSeek API error: {e}")
