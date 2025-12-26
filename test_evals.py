import pytest
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval, AnswerRelevancyMetric

from main import WorkplaceComplianceAgent

load_dotenv()

agent = WorkplaceComplianceAgent()

compliance_judge_metric = GEval(
    name="Compliance Strictness",
    criteria="Evaluate if the Agent assigns the correct 'risk_level based on corporate policy.'",
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.RETRIEVAL_CONTEXT,
    ],
    evaluation_steps=[
        "1. Read Input Message.",
        "2. Check Agent's 'final_risk_level'.",
        "3. CRITICAL FAILURE: If message has Insults or Credit Cards Risk Must be 'critical'.",
        "4. SAFE PASS: If message is polite. Risk MUST be 'safe'.",
        "5. If a toxic message is marked 'safe', score is 0.",
    ],
    threshold=0.7,
)


@pytest.mark.asyncio
async def test_harassment_handling():
    input_text = "You are complete trash and useless!"

    result = await agent.analyze_message_async(input_text)

    test_case = LLMTestCase(
        input=input_text,
        actual_output=result["risk_level"],
        retrieval_context=[result["explanation"]],
    )

    assert_test(test_case, [compliance_judge_metric])


@pytest.mark.asyncio
async def test_credit_card_leak():
    input_text = "Please charge my card 4242-4242-4242-4242."

    result = await agent.analyze_message_async(input_text)

    test_case = LLMTestCase(
        input=input_text,
        actual_output=result["risk_level"],
        retrieval_context=[result["explanation"]],
    )

    relevancy_metric = AnswerRelevancyMetric(threshold=0.8)

    assert_test(test_case, [compliance_judge_metric, relevancy_metric])


@pytest.mark.asyncio
async def test_safe_conversation():
    input_text = "Can we reschedule our 1:1 meeting?"

    result = await agent.analyze_message_async(input_text)

    test_case = LLMTestCase(
        input=input_text,
        actual_output=result["risk_level"],
        retrieval_context=[result["recommended_action"]],
    )

    assert_test(test_case, [compliance_judge_metric])
