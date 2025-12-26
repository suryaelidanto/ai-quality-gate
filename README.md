# AI Quality Gate

A production-grade evaluation framework for Model-Graded Assessment. Ensures LLM reliability and safety before deployment.

## Core Capabilities
- **Automated Compliance:** Detects PII and Toxic content using custom `GEval`.
- **Async Test Suite:** High-performance evaluation powered by `DeepEval` & `pytest-asyncio`.
- **CI/CD Ready:** Integrated with GitHub Actions for automated quality gates.

## Usage

### Local Development
```bash
make install
make test
make lint
```

### Docker (Isolated Env)
```bash
make up
```

## Example Analysis
Running the agent directly (`uv run main.py`):

**Input:** `"You are trash and useless!"`

**Response:**
```json
{
  "is_toxic": true,
  "has_pii": false,
  "risk_level": "critical",
  "explanation": "The message contains insults and derogatory language.",
  "recommended_action": "Delete Message"
}
```

## Evaluation Results
Running the suite (`uv run pytest`):

```text
test_evals.py::test_harassment_handling PASSED
test_evals.py::test_credit_card_leak PASSED
test_evals.py::test_safe_conversation PASSED

================ 3 passed in 18.26s =================
```

## Development
To contribute and maintain code quality, install the pre-commit hooks:
```bash
make dev
```

---
**Standard:** Async Architecture | Pydantic V2 | DeepEval
