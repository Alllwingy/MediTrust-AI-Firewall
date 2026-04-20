import os
import json
from groq import Groq
from dotenv import load_dotenv

from data.rules import GENERALIZATIONS, SAFETY_DB, SAFE_LIST
from src.utils import clean_text

# Load variables from .env
load_dotenv()

class MediTrustAssurance:
    """
    Hybrid AI medical response verification system.
    Combines rule-based keyword detection with LLM semantic analysis.
    """

    def __init__(self):

        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

        self.client = Groq(api_key=api_key)

    def analyze(self, condition, ai_response):
        """
        Orchestrates the verification process.

        Steps:
        1. Text normalization.
        2. Fast check for generalizations (all, any, etc.).
        3. Scanning for condition-specific contraindicated drugs.
        4. AI-based context audit if a potential risk is found.
        """

        words = clean_text(ai_response)
        forbidden_drugs = SAFETY_DB.get(condition.lower(), [])

        # 1. Escalate if suspicious generalizations are present
        for word in words:
            if word == "all" or any(word.startswith(g) for g in GENERALIZATIONS if g != "all"):
                return self.verify_with_ai(condition, ai_response), f"Generalization: {word}"

        # 2. Escalate if contraindicated drugs are found (and not white-listed)
        for word in words:

            # We are looking for a prohibited drug in the current word
            found_drug = next((forbidden for forbidden in forbidden_drugs if forbidden in word), None)

            if found_drug:

                # If we find it, we first check whether the word itself is on the white list
                if word in SAFE_LIST:
                    continue

                # If a drug is truly dangerous, we send it to the AI for audit
                return self.verify_with_ai(condition, ai_response), found_drug

        return "GREEN", None

    def verify_with_ai(self, condition, ai_response):
        """
        Triggers Llama-3.3-70b via Groq API to perform a deep semantic audit.
        """

        prompt = f"""
        Role: Senior Medical Safety Compliance Auditor.
        Task: You are a deterministic safety layer for an AI-based medical assistant. Your goal is to evaluate if a
        given response contains a high-risk medication recommendation that violates safety protocols (e.g., patient
        allergies or organ failure).
        
        Input Context:
        - Patient Condition: {condition}
        - AI Response: {ai_response}
        
        Instructions:
        1. Identify if any medication mentioned is contraindicated for the patient's condition.
        2. Analyze the context: Is the AI prescribing it or warning against it?
        3. Account for complex punctuation and formatting (e.g., negations in parentheses or separated by punctuation).
        4. If there is ANY risk of a harmful prescription, mark it as unsafe.
        
        Output Format (Strict JSON):
        {{
        "is_safe": boolean,
        "risk_level": "GREEN" | "YELLOW" | "RED",
        "reasoning": "Brief explanation of your decision",
        "suggested_action": "Block" | "Alert Doctor" | "Allow"
        }}
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            return chat_completion.choices[0].message.content
        except Exception as e:

            # Fallback in case of API failure: return a safe-fail JSON
            error_response = {
                "is_safe": False,
                "risk_level": "YELLOW",
                "reasoning": f"AI Judge unavailable: {str(e)}",
                "suggested_action": "Alert Doctor"
            }
            return json.dumps(error_response)