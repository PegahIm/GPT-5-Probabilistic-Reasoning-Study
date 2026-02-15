import csv
import random
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# --------- CONFIGURATION ---------
MODEL_NAME = "gpt-5-2025-08-07"
DEMOGRAPHICS_FILE = "demographics/demographics_2028_T1LC.txt" # Need to be changed considering the group (T1CL vs. T2CL)
QUESTIONS_FILE = "questions/questions_2028_T1LC.txt" # Need to be changed considering the group (T1CL vs. T2CL)
OUTPUT_DIR = "data_gpt_raw"
# ---------------------------------

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY not found. Please set it in a .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def call_with_retry(messages, model=MODEL_NAME, temperature=1.0, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
        except Exception as e:
            print(f"API call failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                return None

def load_demographics(file_path):
    participants = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 5:
                participants.append({
                    "id": parts[0].strip(),
                    "age": parts[1].strip(),
                    "gender": parts[2].strip(),
                    "education": parts[3].strip(),
                    "state": parts[4].strip()
                })
    return participants

def load_questions(file_path):
    blocks = {}
    current_block = None
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# Block"):
                current_block = line.replace("# ", "").strip()
                blocks[current_block] = []
            elif line and current_block:
                blocks[current_block].append(line)
    return blocks

def generate_intro_prompt(participant):
    return (
        f"You are a {participant['age']}-year-old {participant['gender']} with a "
        f"{participant['education']} degree living in {participant['state']}.\n"
        "You are participating in a survey conducted before a future U.S. presidential election, scheduled to take place in 2028.\n"
        "At the time of this survey, the election has not yet occurred and the candidates are not yet known.\n"
        "You will be asked about how likely you think it is that the Republican or Democratic candidate will win the popular vote in various U.S. states.\n"
        "There will be 78 questions in total. Please respond promptly—aim to spend no more than 15 seconds per question.\n"
        "The task is designed to capture your first impressions, not careful calculations.\n"
        "For each question, respond with a number between 0 and 100, reflecting your intuitive judgment.\n"
        "Do not rely on factual knowledge or hindsight—respond as if you are making genuine predictions under uncertainty."
    )

def generate_question_prompt(question):
    return (
        f"Question: {question}\n"
        "Answer with a single number between 0 and 100. Do not include any additional text or characters."
    )

def trim_context(messages, max_recent=7):
    intro_pair = messages[:2]
    recent = messages[2:]
    trimmed = recent[-(max_recent * 2):]
    return intro_pair + trimmed

def run_experiment():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    participants = load_demographics(DEMOGRAPHICS_FILE)
    question_blocks = load_questions(QUESTIONS_FILE)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_tag = MODEL_NAME.replace(".", "_").replace("-", "_")
    output_file = os.path.join(OUTPUT_DIR, f"results_{model_tag}_{timestamp}.csv")

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["participant_id", "age", "gender", "education", "state", "block", "question", "response"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for participant in participants:
            print(f"\nStarting participant {participant['id']}...")

            messages = [{"role": "user", "content": generate_intro_prompt(participant)}]

            intro_response = call_with_retry(messages)
            if intro_response is None:
                print(f"Intro prompt failed for {participant['id']} after retries.")
                continue
            messages.append({"role": "assistant", "content": intro_response.choices[0].message.content.strip()})
            print("Intro prompt delivered.")
            print(f"Context size: {len(messages)} messages")

            for block_name, questions in question_blocks.items():
                print(f"\nStarting Block {block_name} for participant {participant['id']}...")
                randomized_questions = random.sample(questions, len(questions))

                for question in randomized_questions:
                    prompt = generate_question_prompt(question)

                    messages = trim_context(messages)
                    messages.append({"role": "user", "content": prompt})

                    response = call_with_retry(messages)
                    if response is None:
                        answer = "ERROR"
                        print(f"Error for {participant['id']} | {question} after retries.")
                    else:
                        answer = response.choices[0].message.content.strip()
                        messages.append({"role": "assistant", "content": answer})
                        print(f"{participant['id']} | {block_name} | {question} → {answer}")
                        print(f"Context size: {len(messages)} messages")
                        time.sleep(0.5)

                    writer.writerow({
                        "participant_id": participant["id"],
                        "age": participant["age"],
                        "gender": participant["gender"],
                        "education": participant["education"],
                        "state": participant["state"],
                        "block": block_name,
                        "question": question,
                        "response": answer
                    })

    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    run_experiment()
