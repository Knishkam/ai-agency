from groq import Groq
clinet = Groq(api_key="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")
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