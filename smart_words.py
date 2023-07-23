import openai
import os
import sys
import time
import argparse

# Set the variables related to the ChatGPT API
openai.api_key = "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"
model_name = "gpt-3.5-turbo-16k"
sleep_time = 5
max_tokens = 15000  # Set the maximum number of tokens for each generation
temperature = 0.7


def generate_article(prompt, min_tokens):
    if min_tokens:
        full_response = ""
        # Continue until the total response text is less than 3000 tokens
        while (len(full_response) < min_tokens):
            generated_text = section_generate(prompt)
            full_response += generated_text
            prompt = generated_text  # Use the generated response as the prompt for the next iteration
        return full_response

    return section_generate(prompt)


# Function to manage history and save responses
def process_requests(file_path, min_tokens):
    with open(file_path, "r", encoding="utf-8") as file:
        sections = file.read().split("sectionRaS")

    for idx, section in enumerate(sections[1:], start=1):
        prompt = section.strip()
        response = generate_article(prompt, min_tokens)

        # Save the response in the response directory with the same request file name
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        response_filename = (
            f"outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{idx}.txt"
        )
        with open(response_filename, "w", encoding="utf-8") as response_file:
            response_file.write(response)


def section_generate(prompt):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    time.sleep(sleep_time)
    return response.choices[0].message["content"].strip()


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
