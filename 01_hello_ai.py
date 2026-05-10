import os
from groq import Groq
clinet = Groq(api_key=os.environ.get("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"))
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