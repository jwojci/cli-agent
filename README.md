# CLI Agent

A command-line AI agent powered by the Google Gemini API that can interact with your file system to execute tasks.

***

## Core Features

* **AI-Powered:** Understands natural language commands to perform file operations.
* **File Management:** Can list, read, and write files within a secure working directory.
* **Code Execution:** Capable of running Python scripts.
* **Example Application:** Includes a simple command-line calculator to demonstrate its capabilities.

***

## Getting Started

### Prerequisites

* Python 3.6+
* Google Gemini API Key

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/cli-agent.git](https://github.com/your-username/cli-agent.git)
    ```
2.  **Install dependencies:**
    ```bash
    pip install google-generativeai python-dotenv
    ```
3.  **Set your API Key:** Create a `.env` file in the `cli_agent` directory and add your key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY"
    ```

### Usage

* **Run the AI Agent:**
    ```bash
    python cli_agent/main.py "your task description here"
    ```
    *Example:* `python cli_agent/main.py "run the calculator tests"`

* **Run the Calculator directly:**
    ```bash
    python cli_agent/calculator/main.py "2 * 3 + 5"
    ```

***

## Testing

To run the included tests for the calculator application, execute:

```bash
python cli_agent/calculator/tests.py

## Potential Improvements
- Advanced Coding Capabilities: Enhance the agent to handle complex bug fixes and perform significant code refactoring.
- Expanded Toolset: Add new functions for the agent to call, such as interacting with external APIs or executing database queries.
- Multi-LLM Support: Abstract the core logic to allow for easy integration with different models (e.g., from Anthropic, local models) for comparison.
- Broader Codebase Compatibility: Improve the agent's effectiveness when operating on larger, unfamiliar codebases with minimal initial context.