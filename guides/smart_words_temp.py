import requests

def get_chatgpt_response(message):
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = "YOUR_TOKEN"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        # "model": "gpt-3.5-turbo",
        "model": "gpt-3.5-turbo-16k",
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": message}]
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    print("Hello! I am ChatGPT. To end the conversation, type 'end'.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "end":
            print("Conversation ended.")
            break

        response = get_chatgpt_response(user_input)
        print("ChatGPT:", response)

if __name__ == "__main__":
    main()
