import openai
import os
import sys
import time

# Set the variables related to the ChatGPT API
openai.api_key = "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"
model_name = "gpt-3.5-turbo-16k"

def generate_article(prompt):
    full_response = ""
    max_tokens = 15000  # Set the maximum number of tokens for each generation

    while len(full_response) < 3000:  # Continue until the total response text is less than 3000 tokens
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        generated_text = response.choices[0].message["content"].strip()
        full_response += generated_text
        prompt = generated_text  # Use the generated response as the prompt for the next iteration
        time.sleep(10)

    return full_response

# Function to manage history and save responses
def process_requests(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        sections = file.read().split("sectionRaS")

    for idx, section in enumerate(sections[1:], start=1):
        prompt = section.strip()
        response = generate_article(prompt)

        # Save the response in the response directory with the same request file name
        if not os.path.exists("response"):
            os.makedirs("response")
        response_filename = f"response/{os.path.splitext(os.path.basename(file_path))[0]}_{idx}.txt"
        with open(response_filename, "w", encoding="utf-8") as response_file:
            response_file.write(response)

if __name__ == "__main__":
    # Scan files in the templates directory and generate articles for each file
    templates_dir = "templates"
    for filename in os.listdir(templates_dir):
        file_path = os.path.join(templates_dir, filename)
        if os.path.isfile(file_path):
            process_requests(file_path)
