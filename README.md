## Project Title: Smart Words
This project is a Python script that leverages the GPT-3.5 Turbo model from OpenAI to generate articles based on provided templates. It allows users to create articles by defining sections, adding prefixes to the sections, and utilizing the power of AI-generated content.

## Features
- Using multiple API keys to reduce the risk of hitting daily rate limits.
- Setting optional minimum and maximum token values for generated sections.
- Adding a set of prefixes to the beginning of all sections of a file when sending a request.
- Displaying detailed information for each section, including the section number, total characters, total words, and the time taken to generate each section.
- Providing the option to save conversation history for each file.

## Prerequisites
- Python 3.6 or higher
- Git (optional, for cloning the repository)

## Installation
1. Clone the repository from GitHub:
   ```
   git clone https://github.com/github-1970/smart-words.git
   cd smart-words
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API keys in the following format:
   ```
   OPENAI_API_KEY_1=YOUR_OPENAI_API_KEY_1
   OPENAI_API_KEY_2=YOUR_OPENAI_API_KEY_2
   OPENAI_API_KEY_3=YOUR_OPENAI_API_KEY_3
   # Add more API keys as needed
   ```

## Usage
1. Prepare your article templates by creating `.txt` files in the `templates` folder. Each template should follow the specified format with `[PREFIX]` and `[SECTION]` markers.

2. Run the main script to generate articles based on the templates:
   ```
   python smart_words.py [--min_tokens MIN_TOKENS] [--max_tokens MAX_TOKENS] [-s]
   ```
   
   Options:
   - `--min_tokens`: Set the minimum number of tokens for each section (optional).
   - `--max_tokens`: Set the maximum number of tokens for each section (default is 15000, optional).
   - `-s`, `--save_conversation_history`: Save the conversation history for each file (optional).

3. The generated articles will be saved in the `outputs` folder. Each article will have its own directory with the same name as the original template file.



## Examples
**Example 1: Generating Articles**
Suppose you have a template file named `file1.txt` with the following content:
```
[PREFIX]
Article Information:
Title: Sample Article
Introduction: This is a sample article template.
Long tail keyword: Sample long tail keyword
Related keywords:
- Keyword 1
- Keyword 2
- Keyword 3

[END_PREFIX]

[SECTION]
Sample content for section 1.
[END_SECTION]

[SECTION]
Sample content for section 2.
[END_SECTION]
```

After running the script, it will generate two articles based on the `file1.txt` template and save them in the `outputs` folder.

**Example 2: Saving Conversation History**
To save conversation history with chatgpt for each file separately, use the `-s` or `--save_conversation_history` option:
```
python smart_words.py -s
```

This will save the conversation history between the user and the AI assistant for each generated article.
> Note: It is recommended not to use this flag too much. Because it increases the amount of text for each request and you may face a rate limit!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions to this project are welcome. Please fork the repository and create a pull request with your suggested changes.

## Credits
This project uses the GPT-3.5 Turbo model provided by OpenAI. For more information about the model, visit the OpenAI website.

## Disclaimer
This project is meant for educational and research purposes only. The AI-generated content may not always be accurate, and it is the user's responsibility to verify the information before using it for any purpose.

## Contact
If you have any questions or suggestions, feel free to contact the project maintainer at rasmor1970@gmail.com.
