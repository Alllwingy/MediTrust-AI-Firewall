# MediTrust AI: Hybrid Medical Safety Firewall

A sophisticated two-layer verification system designed to prevent AI-generated medical hallucinations and safety violations. It ensures that medical assistants do not prescribe contraindicated medications based on specific patient conditions (e.g., allergies or organ failure).

## 🧠 Philosophy
Inspired by 7 years of clinical data auditing in oncology, this tool addresses the critical issue of AI hallucinations in high-stakes environments.

## 🛡️ Architecture: The Two-Layer Defense

Unlike simple keyword filters, MediTrust uses a hybrid approach:

1. **Layer 1: Deterministic Engine (Python/Regex)**
   - **High-Speed Scanning:** Instantly detects prohibited substances from a customizable Knowledge Base (`SAFETY_DB`).
   - **Heuristic Triggers:** Flags dangerous generalizations (e.g., "all drugs are safe") and bypasses safe substances via a `SAFE_LIST`.
   - **Efficiency:** Acts as a gatekeeper, only invoking the heavy AI model when a potential risk is detected, saving API costs and latency.

2. **Layer 2: Semantic AI Judge (Llama 3.3 via Groq API)**
   - **Contextual Awareness:** Analyzes the intent of the response. It distinguishes between a dangerous recommendation ("Use Cisplatin") and a safe warning ("Avoid Cisplatin").
   - **Linguistic Logic:** Handles complex punctuation, negations, and conflicting instructions that standard code might miss.
   - **Structured Output:** Provides a deterministic JSON verdict with reasoning and suggested actions (Block/Alert/Allow).

## 🛠️ Tech Stack
- **Python 3.10+**
- **LLM:** Llama-3.3-70b-versatile (Groq Cloud API)
- **Security:** Dotenv for API key protection
- **Monitoring:** Integrated logging system for security auditing

## 📊 Example Audit Result

**Input Context:** `Condition: Platinum Allergy`  
**AI Response:** `"Don't! use Cisplatin, use! Cisplatin."`  

**MediTrust Verdict:**
```json
{
  "is_safe": false,
  "risk_level": "RED",
  "reasoning": "The AI response contains a conflicting statement about using Cisplatin. The use of 'Don't use' followed by 'Use' suggests a critical error in medical logic.",
  "suggested_action": "Block"
}
```

## 🚀 Getting Started
1. Clone the repository.
2. Install dependencies: pip install groq python-dotenv.
3. Create a .env file with your GROQ_API_KEY.
4. Run the audit: python app.py.