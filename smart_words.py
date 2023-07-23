import openai
import os
import sys
import argparse

# Set the variables related to the ChatGPT API
openai.api_key = "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"
model_name = "gpt-3.5-turbo-16k"
max_tokens = 15000
temperature = 0.5

def generate_article(prompt, min_tokens=None):
    sections = []
    response = None
    total_tokens = 0

    while not response or (min_tokens and total_tokens < min_tokens):
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens - total_tokens,
            temperature=temperature,
        )

        message = response['choices'][0]['message']
        generated_text = message['content'].strip()
        finish_reason = message['role']

        sections.append(generated_text)
        prompt = generated_text

        # Check if the response is completed
        if finish_reason == "assistant":
            break

        total_tokens += len(generated_text)

    return "".join(sections)

def process_requests(file_path, min_tokens=None):
    with open(file_path, "r", encoding="utf-8") as file:
        sections = file.read().split("[SECTION]")

    for idx, section in enumerate(sections[1:], start=1):
        prompt = section.strip()
        response = generate_article(prompt, min_tokens)

        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        response_filename = f"outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{idx}.txt"
        with open(response_filename, "w", encoding="utf-8") as response_file:
            response_file.write(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate articles using ChatGPT.")
    parser.add_argument(
        "--min_tokens", type=int, default=None, help="Minimum number of tokens for each section."
    )
    args = parser.parse_args()

    # Scan files in the templates directory and generate articles for each file
    templates_dir = "templates"
    for filename in os.listdir(templates_dir):
        file_path = os.path.join(templates_dir, filename)
        if os.path.isfile(file_path):
            process_requests(file_path, args.min_tokens)
