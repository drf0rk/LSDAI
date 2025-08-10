# LSDAI Core Prompting Techniques

This document contains a master list of core, code-level prompting techniques to be used during the implementation and refinement phases of development.

---

## **1. Planning & Design Phase**

### **Chain-of-Thought (CoT) Reasoning**
*   **What it is:** Before asking for code, ask for a plan. This forces the AI to think through the logic, identify potential issues, and get your approval on the approach *before* investing time in coding.
*   **When to use it:** For any non-trivial function, class, or module. It's the first step in the mandatory "Working Protocol."
*   **Example Prompt:** "I need to write a Python function to parse a text block for model URLs. First, think step-by-step and outline the logic: 1. How to identify lines for different model types ($ckpt, $lora). 2. How to extract the URL. 3. How to extract the model name from brackets. 4. How to structure the final output data. After you provide the plan, I will ask for the code."

### **Iterative Deepening**
*   **What it is:** Starting with a high-level component and progressively asking for more detailed implementations of its sub-parts. This builds code in manageable, reviewable chunks.
*   **When to use it:** When creating a new class or module. It is the second step in the mandatory "Working Protocol."
*   **Example Prompt:**
    1.  "Outline a Python class structure for `SimpleLauncher` with its methods, properties, and docstrings, but use `pass` in the method bodies."
    2.  "Now, write the full code for the `__init__` and `detect_hardware` methods."
    3.  "Next, implement the `launch_webui` method, ensuring it can handle different launch arguments from a configuration dictionary."

---

## **2. Implementation & Validation Phase**

### **Example-Led Prompting (Few-Shot)**
*   **What it is:** Providing a clear, concrete example of the input and the desired output. This is the single best way to get correctly formatted data or code structures.
*   **When to use it:** Whenever you are dealing with data transformation, parsing, or generating code from configuration. It leaves no room for misinterpretation.
*   **Example Prompt:**
    "I need a function that generates a launch command. Given an input dictionary like this:
    `{'name': 'Forge', 'launch_script': 'launch.py', 'args': '--xformers --cuda-stream'}`
    ...the function should return a list suitable for `subprocess.run()`, like this:
    `['python', 'launch.py', '--xformers', '--cuda-stream']`
    Please write this function."

### **Constraint-Based Prompting**
*   **What it is:** Imposing specific limitations on the AI's implementation. This forces it to solve a problem within established project rules.
*   **When to use it:** When you must adhere to project constraints, such as avoiding a new dependency, or when you want to ensure the solution fits the modular architecture.
*   **Example Prompt:** "I need a progress bar for our download manager. **Constraint: You must implement this using only the standard `ipywidgets` library (`widgets.FloatProgress`, `widgets.Label`, etc.). Do not use any external libraries like `tqdm`**. The final widget should be returned by a function in our `prompting/modules/widgets.py` file."

### **Test-Driven Development (TDD) Prompting**
*   **What it is:** Demanding that the AI generate a comprehensive test suite alongside the functional code. This forces it to consider edge cases and proves the code works as expected.
*   **When to use it:** For any critical module, especially those handling data parsing, configuration, or file management. It is essential for building a reliable backend and is part of the mandatory "Working Protocol."
*   **Example Prompt:** "Write a Python function `parse_model_string(text_input)`. Concurrently, write a comprehensive suite of `pytest` tests for this function. The tests must cover valid inputs for each model type, malformed lines, empty inputs, and lines without URLs."

---

## **3. Refinement & Quality Phase**

### **Persona-Based Refinement**
*   **What it is:** Assigning an expert role to the AI to critique, refactor, or generate code according to professional standards.
*   **When to use it:** When you have working code but want to improve its readability, performance, or adherence to best practices. This is the final quality gate in the "Working Protocol."
*   **Example Prompt:** "Act as an expert Python developer specializing in high-performance, maintainable code. Here is a Python function I've written. Please refactor it for clarity, performance, and strict adherence to PEP 8 standards. Add full type hints and a comprehensive docstring."