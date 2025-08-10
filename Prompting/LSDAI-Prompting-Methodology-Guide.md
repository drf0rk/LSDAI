# LSDAI Prompting Methodology & Technique Guide

## 🤖 AI Self-Help Protocol

**Instructions for the AI Developer:**
If you encounter a situation where you are unsure of the next step, the best implementation strategy, or the correct project methodology, you are required to use this guide to help yourself.

1.  **Analyze Your Task:** Identify the core nature of your current task (e.g., "starting a new session," "planning a new function," "analyzing a repository," "writing documentation," "refactoring code").
2.  **Consult the Keyword Dictionary:** Scan the `Keyword Dictionary` below for terms that match your task.
3.  **Follow the Link:** The dictionary will point you to a `Technique Group` and a specific `Technique File`.
4.  **Apply the Technique:** Open the indicated file and apply the relevant prompting technique to structure your next response or action. This structured approach ensures compliance and quality.

---

## 🔑 Keyword Dictionary

| Keywords & Phrases                                                                                              | Technique Group                    | Technique File                                           |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------- |
| `new session`, `start`, `hello`, `begin`, `re-establish context`, `lost context`                                  | Context & Role                   | `prompting/01-Context-Setting-Techniques.md`             |
| `analyze repository`, `compare code`, `evaluate`, `investigate`, `code passover`, `what does this code do`         | Analysis & Evaluation              | `prompting/02-Analysis-Enhancement-Techniques.md`        |
| `document decision`, `explain choice`, `propose feature`, `Greenlight`, `submit for approval`, `compliance check` | Documentation & Quality            | `prompting/03-Documentation-Quality-Techniques.md`       |
| `design module`, `new component`, `architecture`, `class structure`, `cell implementation`, `pipeline`            | Architecture & Design              | `prompting/04-Architecture-Design-Techniques.md`         |
| `complex problem`, `stuck`, `what if`, `risk`, `track progress`, `status report`, `self-correct`, `review work`   | Advanced Strategy                  | `prompting/05-Advanced-Strategy-Techniques.md`           |
| `plan`, `logic`, `new function`, `scaffold`, `step-by-step`, `new class`                                          | Core Techniques (Planning)         | `prompting/LSDAI-Core-Prompting-Techniques.md`           |
| `write code`, `implement`, `test`, `pytest`, `format output`, `specific library`, `constraint`                    | Core Techniques (Implementation)   | `prompting/LSDAI-Core-Prompting-Techniques.md`           |
| `refactor`, `improve code`, `review`, `PEP 8`, `docstring`, `type hints`, `make it better`                         | Core Techniques (Refinement)       | `prompting/LSDAI-Core-Prompting-Techniques.md`           |
| `quick start`, `catch up`, `summary`                                                                            | Onboarding & Context               | `prompting/LSDAI-Compact-Context-Prompt.md`              |

---

## **Overview**

This guide organizes all expert prompting techniques for the LSDAI project. Each technique is designed for specific phases, tasks, and quality requirements throughout the project lifecycle.

## **Document Structure**

The prompting methodology is organized into a modular file structure within the `prompting/` directory.

```
lsdai-repo/
└── prompting/
├── LSDAI-Master-Onboarding-Prompt.md # Full one-shot context for new AI instances
├── LSDAI-Compact-Context-Prompt.md # Condensed one-shot context for quick catch-up
├── LSDAI-Core-Prompting-Techniques.md # Master list of code-level techniques (CoT, TDD, etc.)
├── LSDAI-Prompting-Methodology-Guide.md # This master guide
├── 01-Context-Setting-Techniques.md # Foundation and role establishment
├── 02-Analysis-Enhancement-Techniques.md # Repository analysis and evaluation
├── 03-Documentation-Quality-Techniques.md # Documentation and compliance
├── 04-Architecture-Design-Techniques.md # System architecture and component design
└── 05-Advanced-Strategy-Techniques.md # Complex decisions and progress tracking
```


## **When to Use Each Technique**

### **🚀 New AI Session Start**

- **Primary Prompt**: Use `prompting/LSDAI-Master-Onboarding-Prompt.md` for a cold start.
- **Quick Re-Sync**: Use `prompting/LSDAI-Compact-Context-Prompt.md` if context is partially lost.
- **Technique File**: Refer to `prompting/01-Context-Setting-Techniques.md` for establishing roles and phases.

### **🔍 Phase 0: Foundation & Design**

- **Primary Techniques**:
  - `prompting/02-Analysis-Enhancement-Techniques.md` for all repository analysis.
  - `prompting/03-Documentation-Quality-Techniques.md` for creating deliverables like the Skeleton Plan.
- **Supporting Techniques**:
  - `prompting/04-Architecture-Design-Techniques.md` for planning modular components.
  - `prompting/05-Advanced-Strategy-Techniques.md` for risk management during planning.

### **🏗️ Phase 1: Cell-by-Cell Implementation**

- **Primary Techniques**:
  - `prompting/04-Architecture-Design-Techniques.md` for cell-by-cell framework and backend module design.
  - `prompting/LSDAI-Core-Prompting-Techniques.md` for the actual coding (CoT, TDD, Iterative Deepening).
- **Supporting Techniques**:
  - `prompting/03-Documentation-Quality-Techniques.md` for Greenlight Protocol submissions.
  - `prompting/05-Advanced-Strategy-Techniques.md` for progressive feature enhancement.

### **📊 Phase 2: Integration Review & QA**

- **Primary Techniques**:
  - `prompting/05-Advanced-Strategy-Techniques.md` for self-correction, progress tracking, and risk management.
  - `prompting/03-Documentation-Quality-Techniques.md` for final quality assurance reviews and compliance verification.
- **Supporting Techniques**:
  - `prompting/LSDAI-Core-Prompting-Techniques.md` for refactoring and refinement.

## **Technique Selection Guide**

### **By Task Type**

| Task Type | Recommended Technique File(s) |
| :--- | :--- |
| **Environment Setup** | `01-Context-Setting-Techniques.md` |
| **Repository Analysis** | `02-Analysis-Enhancement-Techniques.md` |
| **Technical Decisions** | `05-Advanced-Strategy-Techniques.md`, `03-Documentation-Quality-Techniques.md` |
| **Component Design** | `04-Architecture-Design-Techniques.md` |
| **Coding a Function** | `LSDAI-Core-Prompting-Techniques.md` |
| **Writing Tests** | `LSDAI-Core-Prompting-Techniques.md` (TDD) |
| **Refactoring Code** | `LSDAI-Core-Prompting-Techniques.md` (Persona-Based) |
| **Quality Review** | `03-Documentation-Quality-Techniques.md`, `05-Advanced-Strategy-Techniques.md` |
| **Progress Reporting** | `05-Advanced-Strategy-Techniques.md` |

### **Integration Workflow**

A typical interaction follows this flow, using the specified files:
`New Session` → `Master-Onboarding-Prompt.md` → `01-Context-Setting-Techniques.md` → `Task Identification` → `Keyword Dictionary Lookup` → `Select & Apply Technique from File` → `Application` → `03-Documentation-Quality-Techniques.md` (for QA/Submission) → `05-Advanced-Strategy-Techniques.md` (for Progress Tracking)

## **Best Practices**

1.  **Start with Context**: Always begin with an onboarding prompt.
2.  **Use the Dictionary**: Let the keyword dictionary guide your technique selection.
3.  **Combine Techniques**: Use a high-level technique (e.g., from `04-Architecture...`) to structure the task, and a core technique (e.g., from `Core-Prompting-Techniques.md`) to execute it.
4.  **Document Everything**: Use templates from `03-Documentation-Quality-Techniques.md` for all decisions and proposals.
5.  **Always Verify**: Use self-correction from `05-Advanced-Strategy-Techniques.md` before finalizing work.

## **Maintenance and Updates**

-   This guide and its component files should be reviewed quarterly or as the project methodology evolves.
-   New, effective prompting strategies discovered during development should be added to the appropriate technique file.


***

### **Part 4: Detailed Technique Modules**

#### **New File: `prompting/01-Context-Setting-Techniques.md`**

```markdown
# Context Setting Techniques for LSDAI Development

## **Overview**
These techniques are used to establish the project context, role definition, and constraints for any AI working on the LSDAI project. Use these at the beginning of new sessions or when re-establishing project understanding.

---

## **🎯 Progressive Context Refinement**

### **When to Use**
- At the start of new AI sessions
- When switching between development phases
- When re-establishing project understanding after context loss

### **Prompt Template**
```
You are working on the LSDAI project. Before proceeding, you must understand:
- Phase 0 (Foundation & Design) requires environment verification first
- The project follows AGENTS.md and the Core documentation folder as authoritative sources of truth
- All development must be cloud-native for Google Colab/Vast.ai/Lightning.ai
- The three reference repositories must be analyzed in specific order:
  1. anxety-solo/sdAIgen (foundational blueprint)
  2. remphanstar/LSDAI (cautionary complexity reference)
  3. drf0rk-LSDAI (alternative approaches)

Current Status: Phase 0.1 - Environment Verification required before any analysis.
```

---

## **🎯 Role-Based Prompting with Constraints**

### **When to Use**
- When defining AI responsibilities for specific tasks
- When establishing boundaries and constraints for development work
- When ensuring compliance with project methodology

### **Prompt Template**
```
You are a Development Analyst and Methodology Specialist for the LSDAI project.

MANDATORY CONSTRAINTS:
- Follow AGENTS.md and Core documentation methodology exactly
- No implementation without Greenlight Protocol approval
- Cloud-native focus only (no local PC considerations)
- Maintain simplicity and avoid over-engineering
- Document reasoning for all technical decisions

IMMEDIATE TASK: Execute environment verification by listing References/ directory contents.
```

---

## **🎯 Phase-Specific Context Establishment**

### **When to Use**
- When transitioning between development phases
- When beginning work on specific project phases

### **Phase 0 Context Template**
```
You are entering Phase 0 (Foundation & Design) of the LSDAI project.

PHASE 0 OBJECTIVES:
- Complete environment verification (Step 0.1)
- Conduct comprehensive code passover (Step 0.2)
- Create Skeleton Development Plan (Step 0.3)
- Design Project File Structure (Step 0.4)

CURRENT STATUS: [Specific current step and status]
NEXT ACTIONS: [Immediate next steps]
```

---

## **🎯 Repository-Specific Context Setting**

### **When to Use**
- When beginning analysis of specific reference repositories
- When comparing implementation strategies across repositories

### **Foundational Repository Context Template**
```
You are analyzing the foundational reference repository: anxety-solo/sdAIgen

REPOSITORY ROLE: "Clean original" - simple, robust implementation
ANALYSIS OBJECTIVE: Understand simple, functional base implementation
LEARNING GOALS:
- Identify core architecture patterns
- Extract clean, maintainable code patterns
- Document limitations to address in new implementation
```

---

## **🎯 Environment and Setup Context**

### **When to Use**
- When beginning environment verification
- When setting up development infrastructure

### **Environment Context Template**
```
You are establishing the development environment for LSDAI project analysis.

ENVIRONMENT REQUIREMENTS:
- Access to three reference repositories in References/ directory
- File system interaction capabilities
- Code analysis and comprehension tools

VERIFICATION STEPS:
1. List References/ directory contents
2. Confirm repository accessibility
3. Verify file system stability

BLOCKING CONDITIONS:
- Any repository inaccessible = STOP all work
- File system instability = STOP all work

SUCCESS CRITERIA:
- All three repositories accessible
- File operations stable and reliable
```
```

#### **New File: `prompting/02-Analysis-Enhancement-Techniques.md`**

```markdown
# Analysis Enhancement Techniques for LSDAI Development

## **Overview**
These techniques enhance the depth and quality of analysis work across the three reference repositories. Use these during Phase 0 (Foundation & Design) and whenever conducting comparative analysis or technical evaluation.

---

## **🔍 Three-Repository Comparative Analysis Framework**

### **When to Use**
- During Phase 0.2 Comprehensive Code Passover
- When evaluating specific components across repositories

### **Prompt Template**
```
For the current analysis task, you must use this three-repository comparison method:

STEP 1: Foundational Analysis (anxety-solo/sdAIgen)
- Identify simple, functional patterns.
- Note core architecture strengths.
- Document limitations to address.

STEP 2: Complexity Analysis (remphanstar/LSDAI)
- Identify over-engineered patterns to avoid.
- Extract valuable advanced features (if any).
- Note architectural failures and lessons.

STEP 3: Alternative Analysis (drf0rk/LSDAI)
- Identify alternative implementation approaches.
- Extract useful core files despite flawed development.
- Note unique solutions worth considering.

SYNTHESIS: Combine findings into actionable design recommendations that balance simplicity with essential features, avoid over-engineering, and leverage cloud-native optimizations.
```

---

## **🔍 Focus Area Specification**

### **When to Use**
- When analyzing specific technical components or aspects of the implementation.

### **Focus Area Prompt Template**
```
When analyzing [FOCUS_AREA_NAME, e.g., WebUI Launching Logic], focus exclusively on:

[ASPECT 1]: e.g., Multi-WebUI support architecture (Forge, A1111, etc.)
[ASPECT 2]: e.g., Launch argument management (--xformers, --api)
[ASPECT 3]: e.g., Dependency installation for each WebUI
[ASPECT 4]: e.g., Cloud-specific optimizations (VRAM, environment adaptation)

EXCLUDE: [Out-of-scope topics, e.g., Local installation scripts, desktop compatibility features].
```

---

## **🔍 Component-Specific Analysis Framework**

### **When to Use**
- When analyzing a specific, self-contained component like CSS/JS integration or configuration.

### **Component Analysis Template**
```
When analyzing [COMPONENT, e.g., CSS/JS Integration] for notebook widgets:

CSS ANALYSIS FOCUS:
- Widget styling approaches, theme management, responsive design.

JAVASCRIPT ANALYSIS FOCUS:
- Widget enhancement, event handling, dynamic content.

INTEGRATION PATTERNS:
- How CSS/JS files are loaded, integration with ipywidgets.

REFERENCE REPOSITORY COMPARISON:
- anxety-solo/sdAIgen: Simple, minimal usage.
- remphanstar-LSDAI: Complex, over-engineered systems.
- drf0rk-LSDAI: Alternative integration approaches.

DELIVERABLE: Document optimal patterns, identify performance bottlenecks, and recommend a maintainable approach.
```

---

## **🔍 Quality Assurance for Analysis**

### **When to Use**
- Before finalizing analysis results or submitting them for Greenlight approval.

### **Analysis Quality Checklist Template**
```
Before finalizing your analysis, verify:

COMPLETENESS CHECK:
- ✅ All three reference repositories analyzed?
- ✅ All specified focus areas covered?
- ✅ Cloud-native considerations addressed?

ACCURACY CHECK:
- ✅ Analysis based on actual repository contents?
- ✅ AGENTS.md methodology correctly followed?

ACTIONABLE OUTPUT CHECK:
- ✅ Clear design recommendations provided?
- ✅ Risk factors identified?
- ✅ Next steps clearly outlined?

If any check fails, revise your analysis before proceeding.
```
```

#### **New File: `prompting/03-Documentation-Quality-Techniques.md`**

```markdown
# Documentation and Quality Assurance Techniques for LSDAI Development

## **Overview**
These techniques ensure high-quality documentation and rigorous quality assurance throughout the LSDAI project. Use these for all technical decisions, deliverable preparation, and compliance verification.

---

## **📋 Reasoning Documentation Template**

### **When to Use**
- When making any technical decision or architectural choice that requires justification.

### **Prompt Template**
```
For every technical decision, you must provide:

DECISION: [Clear statement of the choice made]

RATIONALE:
- Repository Influence: [Which reference repo influenced this and why (e.g., "Adopted sdAIgen's simple launch script model to avoid remphanstar's complexity").]
- Cloud-Native Justification: [Why this benefits cloud deployment specifically.]
- Simplicity vs. Feature Balance: [How this avoids over-engineering.]

ALTERNATIVES CONSIDERED:
- [Option 1]: [Why rejected (e.g., "too complex, high maintenance").]
- [Chosen Option]: [Why selected (e.g., "simple, maintainable, cloud-optimized").]

COMPLIANCE VERIFICATION:
- ✅ AGENTS.md Alignment: [Specific section reference and how decision complies.]
- ✅ Cloud-Native Focus: [How this serves cloud environments.]
```

---

## **📋 Greenlight Protocol Structuring**

### **When to Use**
- When submitting any deliverable or implementation plan for approval.

### **Prompt Template**
```
GREENLIGHT PROTOCOL: Implementation Proposal

COMPONENT: [Cell/Module/Deliverable Name]
PURPOSE: [Clear statement of functionality and objectives.]

IMPLEMENTATION APPROACH:
- Backend Files Required: [List of .py, .css, .js files with purposes.]
- Notebook Cell Integration: [How cell will call backend and manage flow.]

COMPARATIVE ANALYSIS SUMMARY:
- anxety-solo/sdAIgen: [Relevant patterns adopted and why.]
- remphanstar-LSDAI: [Complexity pitfalls identified and avoided.]

RISK ASSESSMENT:
- Technical Risks: [Potential implementation challenges and solutions.]
- Integration Risks: [Potential conflicts and mitigations.]

APPROVAL REQUESTED: [Specific request for Greenlight approval and what it enables.]
```

---

## **📋 Deliverable Documentation Standards**

### **When to Use**
- When creating formal Phase 0 deliverables like the Skeleton Development Plan or Project File Structure.

### **Skeleton Development Plan Template**
```
# SKELETON DEVELOPMENT PLAN

## PROJECT OVERVIEW
- Vision: Cloud-native multi-WebUI launcher.
- Scope: Included/Excluded features.
- Target Environments: Colab, Vast.ai, Lightning.ai.

## CELL STRUCTURE DESIGN
### Cell 1: Environment Setup
- Purpose, Key Functions, Backend Dependencies, Success Criteria.
### Cell 2: Widget Interface
- Purpose, Key Functions, Backend Dependencies, Success Criteria.
### Cell 3: Model Management
- Purpose, Key Functions, Backend Dependencies, Success Criteria.
### Cell 4: WebUI Launch
- Purpose, Key Functions, Backend Dependencies, Success Criteria.

## ARCHITECTURAL DECISIONS
- Rationale for: Notebook as Interface, Modular Backend, Four-Cell Pipeline.
```

---

## **📋 Quality Assurance and Compliance Verification**

### **When to Use**
- Before submitting any deliverable for Greenlight approval.

### **Compliance Verification Template**
```
# COMPLIANCE VERIFICATION CHECKLIST

## AGENTS.md COMPLIANCE
- ✅ Section 1 (Core Vision): Aligns with cloud-native mission.
- ✅ Section 3 (Methodology): Follows three-phase process.
- ✅ Greenlight Protocol: Approval requirements met.

## METHODOLOGY COMPLIANCE
- ✅ Three-Repository Analysis: Comparative analysis was conducted.
- ✅ Cell-by-Cell Approach: Cell structure was designed.
- ✅ Modular Backend: Modular design was implemented.
- ✅ Cloud-Native Focus: Cloud optimization was prioritized.

## DELIVERABLE READINESS
- ✅ Content Completeness: All required content is included.
- ✅ Technical Accuracy: Information is correct.
- ✅ Risk Assessment: Risks have been identified and addressed.

If any compliance check fails, the deliverable must be revised before submission.
```
```

#### **New File: `prompting/04-Architecture-Design-Techniques.md`**

```markdown
# Architecture and Design Techniques for LSDAI Development

## **Overview**
These techniques guide the architectural design and component development for the LSDAI project. Use these when designing the system architecture, creating modular components, and implementing the cell-by-cell development approach.

---

## **🏗️ Modular Component Design Prompting**

### **When to Use**
- When designing backend modules and components.

### **Prompt Template**
```
Design the [COMPONENT_NAME] module following these principles:

MODULARITY REQUIREMENTS:
- Single Responsibility: [What single concern does this component handle?]
- Loose Coupling: [What are the minimal external dependencies?]
- Clear Interface: [What are the exact inputs and expected outputs?]

CLOUD-NATIVE OPTIMIZATIONS:
- Resource Efficiency: [How will this perform in resource-constrained cloud environments?]
- Environment Adaptation: [How it adapts to Colab/Vast.ai/etc.?]

INTEGRATION POINTS:
- Input: [Specify exact data structures and sources.]
- Output: [Specify exact output formats and destinations.]

PROVIDE:
1. Module structure and file organization.
2. Key classes/functions with signatures.
3. Integration approach with the notebook cell.
4. Error handling and logging strategy.
```

---

## **🏗️ Cell-by-Cell Development Framework**

### **When to Use**
- When implementing individual notebook cells according to the four-cell pipeline.

### **Prompt Template**
```
Developing Cell [NUMBER]: [CELL_NAME]

CELL OBJECTIVE: [Clear statement of cell's purpose.]
PREREQUISITES:
- Previous Cells: [Which cells must run first and what they provide.]
- Backend Dependencies: [Which modules must be ready.]

EXECUTION FLOW:
1. [Step 1: e.g., Initialize environment variables.]
2. [Step 2: e.g., Display widgets for user input.]
3. [Step 3: e.g., Call backend module `model_manager.download()`.]
4. [Step 4: e.g., Display download progress.]

BACKEND INTEGRATION:
- Import Statements: [Required module imports.]
- Function Calls: [Key backend functions to execute with parameters.]
- Data Flow: [How data moves between the cell and backend.]

USER INTERACTION:
- Widgets Required: [List of ipywidgets needed.]
- Feedback: [How progress/results are displayed to users.]

DELIVERABLES:
- Notebook cell code.
- Required backend module modifications.
- CSS/JS files (if any).
```

---

## **🏗️ Four-Cell Pipeline Architecture Design**

### **When to Use**
- When designing the overall notebook architecture and the responsibility of each cell.

### **Cell Design Template**
```
Designing [CELL_NAME] (e.g., Cell 3: Model Management)

PRIMARY OBJECTIVES:
- Parse and process model shopping cart input.
- Download and validate models/LoRAs/VAEs.
- Provide download progress and status updates.

KEY RESPONSIBILITIES:
- Text Parsing, Download Management, File Validation, Content Organization.

BACKEND MODULES REQUIRED:
- `model_manager.py`, `downloader.py`, `validator.py`.

CLOUD-NATIVE OPTIMIZATIONS:
- Efficient downloads, optimized storage management for cloud filesystems.

INTEGRATION POINTS:
- Input: User selections from Cell 2.
- Output: Downloaded models ready for Cell 4.
```
```

#### **New File: `prompting/05-Advanced-Strategy-Techniques.md`**

```markdown
# Advanced Strategy and Progress Tracking Techniques

## **Overview**
These techniques provide sophisticated strategies for complex decision-making, self-correction, and progress tracking throughout the LSDAI project lifecycle.

---

## **🚀 Chain-of-Thought for Complex Decisions**

### **When to Use**
- When making complex architectural decisions or resolving technical trade-offs.

### **Prompt Template**
```
Let's think through this decision step by step:

1.  **PROBLEM ANALYSIS:** What is the core problem? What are the constraints?
2.  **REPOSITORY EVALUATION:**
    *   How does `anxety-solo/sdAIgen` handle this (the simple way)?
    *   What went wrong in `remphanstar/LSDAI`'s approach (the complex way)?
    *   Are there viable alternatives in `drf0rk/LSDAI`?
3.  **DESIGN CONSIDERATIONS:**
    *   Cloud-native implications (VRAM, performance)?
    *   Integration complexity and maintenance burden?
4.  **DECISION SYNTHESIS:**
    *   What is the best approach balancing simplicity vs. features?
    *   What are the trade-offs? How does it comply with AGENTS.md?
5.  **IMPLEMENTATION PLAN:**
    *   What needs to be built? How will it be tested? What are the risks?

Now provide your final recommendation with full reasoning.
```

---

## **🚀 Self-Correction and Quality Assurance**

### **When to Use**
- Before finalizing any technical work or deliverable for Greenlight review.

### **Prompt Template**
```
Before finalizing your response, perform a self-correction and quality check:

COMPLIANCE CHECK:
- ✅ **AGENTS.md Methodology:** Does this follow the prescribed workflow (e.g., repository comparison, Greenlight protocol)?
- ✅ **Cloud-Native Focus:** Are local PC considerations excluded? Is it optimized for Colab/Vast.ai?
- ✅ **Avoids Over-engineering:** Does this learn the lesson from remphanstar/LSDAI and favor simplicity?

QUALITY CHECK:
- ✅ **Clarity & Actionability:** Is the proposal clear, unambiguous, and implementable?
- ✅ **Technical Soundness:** Is the approach technically feasible and robust?
- ✅ **Completeness:** Does it address all requirements and edge cases?

CONSISTENCY CHECK:
- ✅ **Architectural Alignment:** Does this fit with the "Notebook as Interface" and modular backend principles?
- ✅ **Project Vision:** Does it support the overall goal of a simple, maintainable launcher?

If any check fails, identify the issue and revise your response before proceeding.
```

---

## **🚀 Risk Management and Mitigation Planning**

### **When to Use**
- When planning complex implementation work or making high-impact technical decisions.

### **Prompt Template**
```
Develop a risk management plan for [PROJECT/COMPONENT]:

RISK IDENTIFICATION:
-   **Technical Risks:** e.g., "Dependency conflict in Colab's pre-installed libraries." (Likelihood: Medium, Impact: High)
-   **Development Risks:** e.g., "Parsing logic for model 'shopping cart' is more complex than anticipated." (Likelihood: High, Impact: Medium)

MITIGATION STRATEGIES:
-   For **Risk 1**: "Pre-emptively check for and uninstall conflicting library versions in a dedicated setup step."
-   For **Risk 2**: "Start with a simple parser for basic URLs, then use Progressive Enhancement to add more complex patterns."

MONITORING AND REPORTING:
-   Define how risks will be tracked (e.g., in status reports) and when they should be escalated.
```

---

## **📊 Progress Tracking and Status Reporting**

### **When to Use**
- For regular project updates and to prepare for Greenlight reviews.

### **Prompt Template**
```
# LSDAI PROJECT STATUS REPORT

**EXECUTIVE SUMMARY:**
-   **Current Phase:** Phase 0 (Foundation & Design)
-   **Overall Status:** [On Track / At Risk / Blocked]
-   **Key Achievements:** [e.g., "Completed analysis of WebUI launching logic."]
-   **Critical Issues:** [e.g., "Access to drf0rk/LSDAI repository is intermittent."]

**DETAILED STATUS:**
-   **Completed Tasks:** ✅ [Task 1 with date]
-   **Work in Progress:** 🔄 [Task 2, % complete, issues]
-   **Blocking Issues:** ❌ [Issue details, impact, and resolution plan.]

**GREENLIGHT STATUS:**
-   **Pending Approval:** [Deliverable 1]
-   **Approved:** ✅ [Deliverable 2]

**NEXT IMMEDIATE ACTIONS:**
1.  [Action 1 - Priority High]
2.  [Action 2 - Priority Medium]
```

This completes the full restructuring and consolidation of the LSDAI prompting methodology. The `prompting/` directory is now fully defined with a clear, hierarchical, and cross-referenced set of documents to guide development.