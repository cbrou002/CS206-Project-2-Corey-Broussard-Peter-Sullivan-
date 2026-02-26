import os
import re
import json
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

PYTHON_DIR = "python_programs"
STRUCTURE_FILE = "output.txt"
OUTPUT_DIR = "propertiessh"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def parse_structures(structure_text):
    pattern = r"=+\nFile: python_programs/(.*?)\n=+\n(.*?)(?=\n=+\nFile:|\Z)"
    matches = re.findall(pattern, structure_text, re.DOTALL)

    structure_map = {}
    for filename, block in matches:
        structure_map[filename.strip()] = block.strip()

    return structure_map


def build_prompt(source_code, structure_output):
    return f"""
You are extracting structure-aligned semantic properties.

SOURCE CODE:
{source_code}

STRUCTURAL ELEMENTS:
{structure_output}

Instructions:
1. Extract function-level properties first.
2. Then extract branch-level and loop-level refinements.
3. Each property must be expressed in a structured, explicit format that includes::
   - The scope of the property (e.g., function-level or branch-level)
   - function: function name
   - Any conditions / preconditions under which it holds
   - property: short snake_case name
   - A formal or semi-formal statement of the property

4. Only reference structural elements listed above.
5. Output ONLY a valid JSON array.
6. Do NOT include markdown.
7. Do NOT include explanations.
"""


def call_ai(prompt):
    payload = {
        "model": "openai/gpt-3.5-turbo",  # free-tier compatible
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]


def extract_properties(source_code, structure_output):
    prompt = build_prompt(source_code, structure_output)
    content = call_ai(prompt)

    # Clean potential code fences
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]

    # Validate JSON
    try:
        parsed = json.loads(content)
        return json.dumps(parsed, indent=4)
    except json.JSONDecodeError:
        raise ValueError("AI did not return valid JSON")


def main():
    structure_text = read_file(STRUCTURE_FILE)
    structure_map = parse_structures(structure_text)

    for filename, structure_block in structure_map.items():
        source_path = os.path.join(PYTHON_DIR, filename)

        if not os.path.exists(source_path):
            continue

        print(f"Processing {filename}...")

        source_code = read_file(source_path)
        properties_json = extract_properties(source_code, structure_block)

        output_path = os.path.join(
            OUTPUT_DIR,
            filename.replace(".py", "_properties.json")
        )

        with open(output_path, "w") as f:
            f.write(properties_json)


if __name__ == "__main__":
    main()
