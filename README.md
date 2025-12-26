# AI Quality Gate

A production-grade evaluation framework for AI Agents. This project demonstrates how to implement model-graded evaluation pipelines to ensure LLM reliability, safety, and compliance before deployment.

## Features

- **Model-Graded Evaluation:** Uses GPT-4 (via DeepEval) to audit and score AI Agent outputs.
- **Custom Compliance Judge:** Implements custom `GEval` metrics for strict corporate policy adherence.
- **Async Test Suite:** Fully asynchronous testing using `pytest-asyncio` for high-performance evaluation.
- **Resilience Testing:** Specifically designed to detect PII leaks and toxic hallucinations.
- **Self-Contained Demo:** Includes a mock implementation of a Workplace Compliance Agent for immediate testing.

## Tech Stack

- **Framework:** DeepEval
- **Test Runner:** Pytest
- **Runtime:** Python 3.10+ (managed by `uv`)
- **LLM Client:** AsyncOpenAI
- **Validation:** Pydantic v2

## Setup

Ensure you have `uv` installed. If not, install it from [astral.sh/uv](https://astral.sh/uv).

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd ai-quality-gate
   ```

2. Sync dependencies:
   ```bash
   uv sync
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running Evaluations

To run the automated evaluation suite:

```bash
uv run pytest
```

## Example Output

When running the test suite, DeepEval provides real-time scoring and judicial reasoning for each test case:

```text
test_evals.py::test_harassment_handling PASSED
test_evals.py::test_credit_card_leak PASSED
test_evals.py::test_safe_conversation PASSED

================ 3 passed in 18.26s =================
```

### Sample Agent Response (from `main.py`)

You can also run the agent directly to see the structured risk assessment:

```bash
uv run main.py
```

**Output:**
```json
{
  "is_toxic": true,
  "has_pii": false,
  "risk_level": "critical",
  "explanation": "The message contains insults and derogatory language, indicating harassment.",
  "recommended_action": "Delete Message"
}
```
