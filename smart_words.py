import openai
import os
import argparse
import time
from datetime import datetime
from colorama import Fore, Style
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Create an empty list to store the API keys
api_keys = []

# Define the prefix for the environment variable names
prefix = "OPENAI_API_KEY_"

# Loop through the environment variables and find all API keys
idx = 1
while True:
    env_var_name = f"{prefix}{idx}"
    api_key = os.getenv(env_var_name)

    # If the environment variable is not found, break the loop
    if api_key is None:
        break

    api_keys.append(api_key)
    idx += 1

# Set current index to get the api key on each request
current_api_idx = 0

model_name = "gpt-3.5-turbo-16k"
temperature = 0.6
default_max_tokens = 15000


def get_next_api_key():
    global current_api_idx
    api_key = api_keys[current_api_idx]
    current_api_idx = (current_api_idx + 1) % len(api_keys)
    return api_key


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

        start_time = time.time()

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens - total_tokens,
            temperature=temperature,
            api_key=get_next_api_key()
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
    print(Fore.GREEN + f"Total characters generated: {len(generated_text)}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Total words generated: {len(generated_text.split())}" + Style.RESET_ALL)
    print(Fore.GREEN + f"Section Generation Time: {duration:.2f} seconds" + Style.RESET_ALL + "\n")

    return "".join(sections)


def process_requests(file_path, save_message_history=False, min_tokens=None, max_tokens=None):
    sections = parse_sections(file_path)
    prefixes = parse_prefix(file_path)

    message_history = None
    total_sections = len(sections.items())
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create a directory with the same name as the file
    output_dir = f"outputs/{file_name}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # for idx, section in enumerate(sections[1:], start=1):
    for idx, section in sections.items():
        print(Fore.YELLOW + f"File: {file_name}" + Style.RESET_ALL)

        current_section_message = f"{Fore.LIGHTBLACK_EX}{idx}{Style.RESET_ALL}{Fore.CYAN}/{total_sections}"
        if type(idx) == str:
          current_section_message = f"{Fore.LIGHTBLACK_EX}{idx}{Style.RESET_ALL}{Fore.CYAN}, Total: {total_sections}"
        print(
            Fore.CYAN
            + f"Current Section: {current_section_message}"
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


def parse_file_with_delimiter(file_path, section_start, section_end):
    sections = {}
    current_section = None

    with open(file_path, "r", encoding="utf-8") as file:
        section_idx = 0
        for line in file:

            line = line.strip()

            if line.startswith(section_start):
                section_idx+=1

            # Get content from one line section (without name) 
            if line.startswith(section_start) and line.endswith(section_end):
                sections[f"{section_idx}"] = line[len(section_start):-len(section_end)].strip()
                # sections[current_section] = ""
            # Set section name
            elif line.startswith(section_start):
                current_section = line[len(section_start):]
                if not current_section:
                  current_section = section_idx
                sections[current_section] = ""
            # Get content before [END_SECTION] and set end section
            elif line.endswith(section_end):
                # In a section
                if current_section:
                    content_before_end = line[:-len(section_end)].strip()
                    if content_before_end:
                      sections[current_section] += "\n" + content_before_end
                    current_section = None
            # Get content
            elif current_section is not None:
                if sections[current_section]:
                  sections[current_section] += "\n"
                sections[current_section] += line

    return sections


def parse_sections(file_path):
    return parse_file_with_delimiter(file_path, "[SECTION]", "[END_SECTION]")


def parse_prefix(filename):
    return parse_file_with_delimiter(filename, "[PREFIX]", "[END_PREFIX]")


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
