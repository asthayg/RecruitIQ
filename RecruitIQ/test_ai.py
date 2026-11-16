import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Hello! Tell me your name."
        }
    ]
)

print(response["message"]["content"])