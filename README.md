# AI_Agent_-chat-based-

# 💳 AI Payment Collection Agent

## 📌 Overview

This project implements a **deterministic conversational AI agent** for handling payment collection workflows.
The agent supports:
- Account lookup
- Identity verification (strict rules)
- Payment processing
- Error handling and retry limits

## Note: Future Enhancements
This is a baseline project that can be further enhanced to improve the quality of the AI agent.
The current system is designed as a reliable and deterministic baseline. Future improvements may include:
- Integration of LLMs for advanced natural language understanding
- Enhanced security and fraud detection mechanisms
- Persistent storage and logging
- Deployment-ready architecture with scalable backend services

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

6. # Demo Use
ACC1001
Nithin Jain
1990-05-14
500
4532015112830366
Nithin Jain
123
12 2027



## 📁 Project Structure & Responsibilities

This project is organized using a modular architecture to separate concerns and ensure maintainability.

---

### 🧠 agent/

Contains the **core logic of the system**.

#### 📄 agent/agent.py
- Main brain of the application
- Implements a **deterministic state machine**
- Handles:
  - Conversation flow
  - State transitions
  - Context management
  - Retry logic
  - Input validation
- Key methods:
  - `next()` → entry point for every user input
  - `_extract_entities()` → parses structured data (account_id, amount, etc.)
  - `_handle_*()` → handles each state (verification, payment, etc.)
  - `_response()` → formats output

---

### 🔌 api/

Handles all **external API communication**.

#### 📄 api/client.py
- Responsible for interacting with external services
- Functions:
  - `lookup_account()` → fetch account details
  - `process_payment()` → processes payment transaction
- Uses HTTP requests (`requests` library)
- Includes basic error handling for network failures

---

### ⚙️ utils/

Contains **supporting utilities and shared logic**.

#### 📄 utils/state.py
- Defines all possible states of the agent
- Implemented using an Enum
- Examples:
  - START
  - VERIFY_NAME
  - VERIFY_SECONDARY
  - SHOW_BALANCE
  - CARD_FLOW
  - END

#### 📄 utils/validators.py (if used)
- Contains reusable validation functions
- Example:
  - card validation
  - amount validation

---

### 🧪 tests/

Contains **test scenarios to validate system behavior**.

#### 📄 tests/test_flows.py
- Simulates real-world interactions
- Covers:
  - Successful payment flow
  - Verification failure
  - Zero balance case
  - Payment failure
- Helps ensure:
  - Correct state transitions
  - Robust error handling
  - No crashes

---

### 💻 app.py

Streamlit-based UI for interactive testing.

- Provides a chat interface
- Maintains session state
- Sends user input to agent
- Displays responses
- Used for demonstration purposes

---

### 🖥️ run.py

Command-line interface (CLI) for the agent.

- Allows manual interaction via terminal
- Useful for quick testing without UI
- Example:



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
