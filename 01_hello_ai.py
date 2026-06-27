import os
from groq import Groq
clinet = Groq(api_key=os.environ.get("GROQ_API_KEY"))
response = clinet.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content":"Hello! Mera name hai shivam hai!"
        }
    ]
)
print(response.choices[0].message.content)