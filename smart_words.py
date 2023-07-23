import openai
import os
import sys
import argparse
import time
from datetime import datetime
from colorama import Fore, Style

# Set the variables related to the ChatGPT API
openai.api_key = "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"
model_name = "gpt-3.5-turbo-16k"
max_tokens = 15000
temperature = 0.6


def generate_article(prompt, message_history=None, min_tokens=None):
    sections = []
    response = None
    total_tokens = 0

    while not response or (min_tokens and total_tokens < min_tokens):
        if message_history:
            messages = message_history.copy()
            messages.append({"role": "user", "content": prompt})
        else:
            messages = [{"role": "user", "content": prompt}]

        start_time = time.time()

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens - total_tokens,
            temperature=temperature,
        )

        end_time = time.time()
        duration = end_time - start_time

        message = response["choices"][0]["message"]
        generated_text = message["content"].strip()
        finish_reason = message["role"]

        sections.append(generated_text)
        prompt = generated_text

        total_tokens += len(generated_text)

        # Check if the response is completed
        if finish_reason == "assistant":
            break

    # Print details for each section
    print(
        Fore.GREEN
        + f"Total characters generated: {len(generated_text)}"
        + Style.RESET_ALL
    )
    print(
        Fore.GREEN
        + f"Total words generated: {len(generated_text.split())}"
        + Style.RESET_ALL
    )
    print(
        Fore.GREEN
        + f"Section Generation Time: {duration:.2f} seconds"
        + Style.RESET_ALL
        + "\n"
    )

    return "".join(sections)


def process_requests(file_path, min_tokens=None, save_message_history=False):
    with open(file_path, "r", encoding="utf-8") as file:
        sections = file.read().split("[SECTION]")

    message_history = None
    total_sections = len(sections) - 1

    for idx, section in enumerate(sections[1:], start=1):
        print(
            Fore.CYAN
            + f"Current Section: {Fore.LIGHTBLACK_EX}{idx}{Style.RESET_ALL}{Fore.CYAN}/{total_sections}"
            + Style.RESET_ALL
        )
        prompt = section.strip()
        if save_message_history:
            response = generate_article(prompt, message_history, min_tokens)
        else:
            response = generate_article(prompt, None, min_tokens)

        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        response_filename = (
            f"outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{idx}.txt"
        )
        with open(response_filename, "w", encoding="utf-8") as response_file:
            response_file.write(response)

        # Update message history with the current response
        if save_message_history:
            if message_history:
                message_history.append({"role": "assistant", "content": response})
            else:
                message_history = [{"role": "assistant", "content": response}]

            # Add a newline after each message history
            message_history[-1]["content"] += "\n"


if __name__ == "__main__":
    start_time = datetime.now()

    parser = argparse.ArgumentParser(description="Generate articles using ChatGPT.")
    parser.add_argument(
        "--min_tokens",
        type=int,
        default=None,
        help="Minimum number of tokens for each section.",
    )
    parser.add_argument(
        "--save_message_history",
        action="store_true",
        help="Whether to save message history for each file.",
    )
    args = parser.parse_args()

    # Scan files in the templates directory and generate articles for each file
    templates_dir = "templates"
    for filename in os.listdir(templates_dir):
        file_path = os.path.join(templates_dir, filename)
        if os.path.isfile(file_path):
            process_requests(file_path, args.min_tokens, args.save_message_history)

    end_time = datetime.now()
    total_time = end_time - start_time
    # Convert total_time to the desired format
    total_time_str = str(total_time)[:-4]
    print(Fore.MAGENTA + f"Total Execution Time: {total_time_str}" + Style.RESET_ALL)
