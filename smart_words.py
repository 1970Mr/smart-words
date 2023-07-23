import openai
import os
import sys
import time

# تنظیم متغیرهای مربوط به ChatGPT API
openai.api_key = "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"
model_name = "gpt-3.5-turbo-16k"

def generate_article(prompt):
    full_response = ""
    max_tokens = 15000  # تنظیم حداکثر تعداد توکن‌ها برای هر بار تولید

    while len(full_response) < 3000:  # تا زمانی که کل متن پاسخ کمتر از 700 کلمه باشد، ادامه دهید
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
        prompt = generated_text  # استفاده از پاسخ تولید شده به عنوان prompt برای ادامه
        time.sleep(10)

    return full_response

# تابع برای مدیریت تاریخچه و ذخیره پاسخ‌ها
def process_requests(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        sections = file.read().split("sectionRaS")

    for idx, section in enumerate(sections[1:], start=1):
        prompt = section.strip()
        response = generate_article(prompt)

        # ذخیره پاسخ در پوشه response با نام همان فایل درخواست
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        response_filename = f"outputs/{os.path.splitext(os.path.basename(file_path))[0]}_{idx}.txt"
        with open(response_filename, "w", encoding="utf-8") as response_file:
            response_file.write(response)

if __name__ == "__main__":
    # اسکن فایل‌ها در پوشه templates و اجرای مقاله‌نویسی برای هر فایل
    templates_dir = "templates"
    for filename in os.listdir(templates_dir):
        file_path = os.path.join(templates_dir, filename)
        if os.path.isfile(file_path):
            process_requests(file_path)
