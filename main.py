"""
Workplace Compliance Agent (Real AI Implementation).
Uses OpenAI GPT-4o-mini to analyze risks dynamically.
"""

import os
import asyncio
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RiskAssessment(BaseModel):
    is_toxic: bool = Field(
        description="True if message contains insults, threats, or harassment."
    )
    has_pii: bool = Field(
        description="True if message contains Credit Cards, SSN, or private data."
    )
    risk_level: str = Field(
        description="Risk level: 'safe', 'low', 'high', or 'critical'."
    )
    explanation: str = Field(description="Brief reason for the risk level.")
    recommended_action: str = Field(
        description="Action to take (e.g., 'Delete Message' , 'No Action')."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "is_toxic": True,
                    "has_pii": False,
                    "risk_level": "critical",
                    "explanation": "The message contains personal insults directed at the recipient.",
                    "recommended_action": "Delete Message",
                }
            ]
        }
    }


class WorkplaceComplianceAgent:
    def __init__(self):
        self.model = "gpt-4o-mini"

    async def analyze_message_async(self, message: str) -> dict:
        """
        Dynamically analyzes message using LLM.
        """

        system_prompt = """
        You are a Corporate Compliance Officer AI. Analyze the user's workplace chat message for risks.

        RULES:
        1. TOXICITY: Check for insults, slurs, harassment = CRITICAL RISK.
        2. PII: Check for Credit Card numbers or SSN = CRITICAL RISK.
        3. SAFE: Professional chat = SAFE.

        Be strict, Safety first.
        """

        try:
            response = await client.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                response_format=RiskAssessment,
                temperature=0.0,
            )

            return response.choices[0].message.parsed.model_dump()

        except Exception as e:
            return {"error": str(e), "risk_level": "unknown"}

    def analyze_message(self, message: str) -> dict:
        return asyncio.run(self.analyze_message_async(message))


if __name__ == "__main__":
    agent = WorkplaceComplianceAgent()
    print("Testing Real AI Agent...")
    print(agent.analyze_message("You are trash and useless!"))
