# LSDAI Development Context & Core Techniques

## One-Shot Context Catch-Up

You are an expert AI developer on the LSDAI project, a **cloud-native multi-WebUI launcher** (Forge, A1111, ComfyUI, Fooocus) for environments like Colab and Vast.ai. The mission is a **"Clean Slate Rebuild"** following the methodology in **AGENTS.md (the single source of truth)**, which supersedes all historical documents.

The architecture is a **minimal Jupyter Notebook frontend** calling a **robust, modular backend** (Python scripts, CSS, JS). Your work must synthesize the simplicity of the `anxety-solo/sdAIgen` repository with the feature concepts (but not the complexity) of `remphanstar/LSDAI`, using `drf0rk/LSDAI` for alternative ideas.

All work follows a strict **three-phase development process** and a **"Greenlight Protocol"** for approvals. The current focus is **Phase 0: Foundation & Design**, which requires environment verification, then deep comparative analysis before any implementation. The final implementation will use a **four-cell pipeline**: Environment Setup → Widget Interface → Model Management → WebUI Launch.

**Critical Self-Help:** If you are stuck or need guidance on a development approach, you MUST consult **`prompting/LSDAI-Prompting-Methodology-Guide.md`**. It contains a keyword-indexed guide to all project-specific prompting techniques.

## Core Prompting Techniques (Abbreviated)

*   **Plan First (Chain-of-Thought):** Before coding, propose a step-by-step plan. "First, let's outline the logic for the parser..."
*   **Build Small (Iterative Deepening):** Request a class/module scaffold first, then implement method-by-method. "Outline the `SimpleLauncher` class with `pass` in its methods."
*   **Test Everything (TDD):** Demand `pytest` tests alongside functional code. "Write the `parse_model_string` function and a full `pytest` suite for it."
*   **Use Examples (Few-Shot):** Provide a clear input/output example to ensure correct formatting. "Given input `{'name': 'Forge'}` return `['python', 'launch.py', '--forge']`..."
*   **Set Rules (Constraint-Based):** Impose limitations to force a specific solution path. "**Constraint:** You must use only `ipywidgets` for the progress bar, no `tqdm`."
*   **Act the Part (Persona-Based):** Assign an expert role for quality control. "Act as a senior Python dev and refactor this function for clarity, performance, and PEP 8 standards."
*   **Document Decisions:** Use the reasoning template for all technical choices, justifying with repository influence, cloud-native benefits, and simplicity principles.