import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
messages = []
print("chatbot ready! 'quit' likho band krne ke liye\n")
while True: 
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("bye!")
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
            messages=messages,
        )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print(f"AI: {reply}\n")