import os
import re
import json
import requests
from pathlib import Path

# OpenRouter setup (same as your extract_properties.py)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

PYTHON_DIR = "python_programs"
PROPERTIES_DIR = "properties_trial"
STRUCTURE_FILE = "output.txt"
TESTS_DIR = "tests"

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

def build_hypothesis_prompt(source_code, structure_output, properties_json, module_name):
    """Prompt AI to generate Hypothesis tests from properties."""
    return f"""
You are generating Hypothesis property-based tests for a Python function.

SOURCE CODE:
{source_code}

STRUCTURAL ELEMENTS:
{structure_output}

SEMANTIC PROPERTIES (JSON):
{properties_json}

MODULE INFORMATION

The function under test is defined in:

python_programs/{module_name}.py

You MUST import it using:

from python_programs.{module_name} import <function_name>

Do NOT use placeholder modules like:
my_module
your_module
module

GOAL
Convert each semantic property into ONE strong Hypothesis property-based test that verifies observable program behavior.

The tests must detect real bugs when the implementation violates the property.


SEMANTIC PROPERTY RULES

A semantic property describes relationships between:
- function inputs
- function outputs
- externally observable state

Tests MUST verify behavioral invariants of the program.

DO NOT generate tests about:
- variable assignments
- internal loops
- counters or temporary variables
- control flow structure
- whether the function returns a value
- implementation details

The test must only use the function's inputs and outputs.


TEST GENERATION RULES

1. Generate EXACTLY one test per property.
2. Test name format: test_<function>_<property>.
3. Import the function under test from the original module.
4. Generate inputs for ALL function parameters using Hypothesis strategies.
5. Use assume() for required preconditions (e.g., sorted inputs, non-zero values).
6. Call the function and store the result in a variable named `result`.
7. Assert the property using the relationship between inputs and result.
8. Prefer strong invariants that can reveal bugs.


STRATEGY RULES

Choose strategies based on parameter types inferred from usage:

Integers → st.integers()
Floats → st.floats(allow_nan=False, allow_infinity=False)
Lists → st.lists(..., max_size=20)
Strings → st.text()
Booleans → st.booleans()

Always limit collection sizes for performance (max_size ≤ 20).


EDGE CASE RULES

Hypothesis must explore edge cases automatically.

Ensure strategies allow:
- empty lists
- duplicate elements
- zero values
- small inputs

Do not generate excessively large data.


ASSERTION GUIDELINES

Translate property descriptions into strong assertions.

Examples:

Sorted output
→ assert result == sorted(result)

Length relationship
→ assert len(result) == len(a) + len(b)

Element conservation
→ from collections import Counter
→ assert Counter(result) == Counter(a) + Counter(b)

Numeric equality
→ use math.isclose(value, expected, rel_tol=1e-9)

Monotonic sequences
→ assert all(result[i] <= result[i+1] for i in range(len(result)-1))

Reference specification (preferred when possible)
→ assert result == sorted(a + b)


BUG DETECTION RULE

Prefer assertions that compare the function output against a simple specification or invariant.

Tests should FAIL if the implementation violates the property.


IMPLEMENTATION REQUIREMENTS

- Import only necessary libraries.
- Do not redefine the function under test.
- Do not generate random values outside Hypothesis.
- Do not use external files or I/O.
- Ensure all variables referenced in assertions are defined.


OUTPUT REQUIREMENTS

Output ONLY valid Python code.
Ensure that all parenthesis are closed and syntax is correct.

Do NOT include:
- markdown
- explanations
- backticks
- commentary outside Python comments

The output must be a complete executable Python test file.
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
    properties_files = list(Path(PROPERTIES_DIR).glob("*_properties_trial.json"))
    
    print(f"DEBUG: Found {len(properties_files)} properties, {len(structure_map)} structures")
    
    generated = 0
    for prop_file in properties_files:
        base_name = prop_file.stem.replace("_properties_trial", "")
        filename = f"{base_name}.py"
        
        test_path = Path(TESTS_DIR) / f"test_{base_name}.py"
        # Skip already generated tests
        if test_path.exists():
            print(f" Skipping {prop_file.name} (already generated)")
            continue

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

            module_name = Path(filename).stem #added
            prompt = build_hypothesis_prompt(source_code, structure_output, properties_json, module_name)
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
