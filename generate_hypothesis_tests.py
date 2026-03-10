import os
import re
import json
import requests
from pathlib import Path

# OpenRouter setup (same as your extract_properties.py)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

PYTHON_DIR = "python_programs"
PROPERTIES_DIR = "properties"
STRUCTURE_FILE = "output.txt"
TESTS_DIR = "hypothesis_tests"

os.makedirs(TESTS_DIR, exist_ok=True)

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def parse_structures(structure_text):
    """Parse structure output.txt into filename → structure mapping."""
    pattern = r"=+\s*\nFile:\s*python_programs[/\\](.*?)\s*\n=+.*?(\n.*?)(?==+\s*\nFile:|\Z)"
    matches = re.findall(pattern, structure_text, re.DOTALL | re.MULTILINE)
    structure_map = {}
    for filepath, block in matches:
        filename = Path(filepath.strip()).name
        structure_map[filename] = block.strip()
    return structure_map

def build_hypothesis_prompt(source_code, structure_output, properties_json):
    """Prompt AI to generate Hypothesis tests from properties."""
    return f"""
You are generating Hypothesis property-based tests for the given Python program.

SOURCE CODE:
{source_code}

STRUCTURAL ELEMENTS:
{structure_output}

SEMANTIC PROPERTIES (JSON):
{properties_json}

TASK: Generate COMPLETE, EXECUTABLE Hypothesis tests for these properties.

REQUIREMENTS:
1. Use @given with appropriate strategies (st.lists, st.integers, st.floats, etc.)
2. Use 'assume()' for preconditions (e.g., assume(sum(xs) != 0))
3. Handle edge cases (empty lists, zero sums, etc.) using structural info
4. Include imports: hypothesis, strategies as st, math (for isclose)
5. Tests must reference functions by exact name from structures
6. Comment generators used (e.g., "Generator: st.lists(st.floats(), min_size=1)")
7. Use math.isclose() for floats with rel_tol=1e-9

OUTPUT ONLY:
- Valid Python test file content
- NO markdown, explanations, or wrappers
- Multiple @given tests if multiple properties

EXAMPLE FORMAT:
import math
from hypothesis import given, assume, strategies as st

def normalize(xs): # Copy function signature from source
# ... (copy relevant function body if needed)

@given(st.just([])) # Generator: always empty list (Branch: len(xs)==0)
    def test_normalize_identity_empty(xs):
    assert normalize(xs) == xs

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_normalize_unit_sum(xs):
    assume(sum(xs) != 0)
    ys = normalize(xs)
    assert math.isclose(sum(ys), 1.0, rel_tol=1e-9)

"""

def call_ai(prompt):
    payload = {
        "model": "openai/gpt-3.5-turbo",  # Better at code gen
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")
    return response.json()["choices"][0]["message"]["content"]

def clean_python_code(content):
    """Remove markdown/python code blocks."""
    content = content.strip()
    # Remove ```python wrappers
    if content.startswith("```python"):
        content = content.split("```python", 1)[1].rsplit("```", 1)[0]
    elif content.startswith("```"):
        content = content.split("```", 1)[1].rsplit("```", 1)[0]
    return content.strip()

def generate_tests():
    print(" Parsing structures...")
    structure_text = read_file(STRUCTURE_FILE)
    structure_map = parse_structures(structure_text)
    
    print(" Reading properties...")
    properties_files = list(Path(PROPERTIES_DIR).glob("*_properties.json"))
    
    print(f"DEBUG: Found {len(properties_files)} properties, {len(structure_map)} structures")
    
    generated = 0
    for prop_file in properties_files:
        base_name = prop_file.stem.replace("_properties", "")
        filename = f"{base_name}.py"
        
        # Flexible matching
        candidates = [k for k in structure_map.keys() if base_name in k or filename in k]
        if not candidates:
            print(f"  Skipping {prop_file.name} (no structure match)")
            print(f"    Looking for: {base_name}.py in {list(structure_map.keys())}")
            continue
        
        filename = candidates[0]  # First match
        print(f" Processing {prop_file.name} → {filename}")
        
        try:
            source_path = Path(PYTHON_DIR) / filename
            if not source_path.exists():
                print(f"     Source missing: {source_path}")
                continue
                
            source_code = read_file(source_path)
            structure_output = structure_map[filename]
            properties_json = read_file(prop_file)
            
            prompt = build_hypothesis_prompt(source_code, structure_output, properties_json)
            ai_response = call_ai(prompt)
            test_code = clean_python_code(ai_response)
            
            test_path = Path(TESTS_DIR) / f"test_{base_name}.py"
            with open(test_path, "w") as f:
                f.write(test_code)
            
            print(f"{generated + 1}. Saved: test_{base_name}.py")
            generated += 1
            
        except Exception as e:
            print(f" Error {prop_file.name}: {e}")
    
    print(f"\n Generated {generated} test files!")

def run_tests():
    """Run all generated tests and report outcomes."""
    import subprocess
    import pytest
    
    print(" Running Hypothesis tests...")
    results = []
    
    for test_file in Path(TESTS_DIR).glob("test_*.py"):
        print(f"\n Testing {test_file}...")
        try:
            result = subprocess.run(
                ["pytest", str(test_file), "-v", "--tb=short"],
                capture_output=True, text=True, timeout=30
            )
            status = "PASS" if result.returncode == 0 else "FAIL"
            results.append({
                "file": test_file.name,
                "status": status,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
            print(f"   {status}: {result.stdout.strip() or 'No output'}")
        except subprocess.TimeoutExpired:
            results.append({"file": test_file.name, "status": "TIMEOUT"})
            print("    TIMEOUT")
    
    # Save results
    with open("test_outcomes.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n Results saved to test_outcomes.json")

if __name__ == "__main__":
    if not OPENROUTER_API_KEY:
        print(" Set OPENROUTER_API_KEY environment variable")
        exit(1)
    
    generate_tests()
    # Uncomment to auto-run tests:
    # run_tests()
