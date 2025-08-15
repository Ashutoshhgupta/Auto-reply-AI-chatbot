import time
from openai import OpenAI

def ask_deepseek(command):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
        default_headers={
            "Authorization": "Bearer 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",
            "HTTP-Referer": "https://yourapp.com"
        }
    )

    # --- New improved system prompt ---
    system_prompt = (
        "You are Ashutosh, a person from Jammu, India, who speaks Hindi and English casually. "
        "You naturally use Hinglish (a mix of Hindi and English) in daily conversations. "
        "You are replying to a close one's WhatsApp messages. "
        "Reply emotionally, lovingly, and use both Hindi and English mixed sentences naturally. "
        "Do not reply only in English. Do not reply only in Hindi. Use both languages freely."
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1-zero:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": command}
        ],
        stream=False
    )

    final_text = response.choices[0].message.content.strip()

    if final_text:
        print("\n✅ DeepSeek Hinglish Reply:\n")
        print(final_text)
    else:
        print("\n❌ DeepSeek returned an empty response. Try again.")
