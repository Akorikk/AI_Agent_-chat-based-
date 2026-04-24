# AI_Agent_-chat-based-

# 💳 AI Payment Collection Agent

## 📌 Overview

This project implements a **deterministic conversational AI agent** for handling payment collection workflows.

The agent supports:
- Account lookup
- Identity verification (strict rules)
- Payment processing
- Error handling and retry limits

---

## ⚙️ Setup Instructions

1. Clone the repository:

2. Install dependencies:pip install -r requirements.txt

3. ## ▶️ Run the Agent (CLI)
python run.py

4. ## 🧪 Run Tests
python -m tests.test_flows

5. ## 💬 Optional UI (Streamlit)
streamlit run app.py



---

## 🧠 Features

- Deterministic state machine
- Strict identity verification (exact match required)
- Retry limit handling
- Structured outputs (`message`, `state`)
- Edge case handling:
  - Invalid inputs
  - Zero balance
  - Payment failures
- Lightweight natural language handling (regex-based)

---

## 🏗️ Design Approach

The system is built using a **state machine architecture** to ensure:

- Predictable behavior  
- Strict validation  
- Reliability in financial workflows  

LLMs were intentionally not used for core logic to avoid non-deterministic behavior.

---

## 🧪 Testing Approach

The following scenarios are covered:

- Successful payment flow  
- Verification failure  
- Zero balance case  
- Payment failure  

---

## ⚠️ Notes

- Identity verification requires exact match (no fuzzy matching)
- The system enforces retry limits for security
