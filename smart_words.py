import openai
import os
import argparse
from datetime import datetime
from colorama import Fore, Style
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Set the API key for OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = "gpt-3.5-turbo-16k"
temperature = 0.6
default_max_tokens = 15000


def generate_article(prompt, message_history=None, min_tokens=None, max_tokens=None):
    sections = []
    response = None
    total_tokens = 0

    while not response or (min_tokens and total_tokens < min_tokens):
        if message_history:
            messages = message_history.copy()
            messages.append({"role": "user", "content": prompt})
        else:
            messages = [{"role": "user", "content": prompt}]

        start_time = datetime.now()

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens - total_tokens,
            temperature=temperature,
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

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
    print(Fore.GREEN + f"Total characters generated: {len(generated_text)}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Total words generated: {len(generated_text.split())}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Section Generation Time: {duration:.2f} seconds" + Style.RESET_ALL + "\n")

    return "".join(sections)


def process_requests(file_path, save_message_history=False, min_tokens=None, max_tokens=None):
    with open(file_path, "r", encoding="utf-8") as file:
        sections = file.read().split("[SECTION]")

    message_history = None
    total_sections = len(sections) - 1
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create a directory with the same name as the file
    output_dir = f"outputs/{file_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, section in enumerate(sections[1:], start=1):
        print(Fore.YELLOW + f"File: {file_name}" + Style.RESET_ALL)
        print(
            Fore.CYAN
            + f"Current Section: {Fore.LIGHTBLACK_EX}{idx}{Style.RESET_ALL}{Fore.CYAN}/{total_sections}"
            + Style.RESET_ALL
        )
        prompt = section.strip()
        if save_message_history:
            response = generate_article(prompt, message_history, min_tokens, max_tokens)
        else:
            response = generate_article(prompt, None, min_tokens, max_tokens)

        # Save the response in the corresponding file directory
        response_filename = f"{output_dir}/{file_name}_{idx}.txt"
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
        "--min_tokens", type=int, default=None, help="Minimum number of tokens for each section."
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=default_max_tokens,
        help="Maximum number of tokens for each section.",
    )
    parser.add_argument(
        "-s",
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
            process_requests(file_path, args.save_message_history, args.min_tokens, args.max_tokens)

    end_time = datetime.now()
    total_time = end_time - start_time
    # Convert total_time to the desired format
    total_time_str = str(total_time)[:-4]
    print(Fore.MAGENTA + f"Total Execution Time: {total_time_str}" + Style.RESET_ALL)
