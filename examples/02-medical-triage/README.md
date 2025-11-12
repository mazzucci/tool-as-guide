# 🏥 Medical Triage - Tool-as-Guide Pattern with Autonomous Agent

> **⚠️ DISCLAIMER**: This is a simplified demonstration for educational purposes only. Real medical systems require clinical expertise, regulatory approval, and extensive validation. This is NOT production medical software.

A demonstration of the **Tool-as-Guide pattern** using an autonomous agent to perform medical triage while following strict clinical protocols.

---

## What This Demonstrates

### The Key Insight

This shows the Tool-as-Guide pattern with an **autonomous agent**:

- **Guide Controls Workflow**: What steps to take, what order, what's mandatory
- **Agent Controls Execution**: How to gather data, which tools to call, how to process results

**The agent is autonomous but the protocol is enforced.**

---

## Architecture

```
Patient → Agent → Guide → Protocol Decision
          ↓              ↓
        Tools       Next Step
        (DB, Vitals)
```

### How It Works

1. **Agent receives task from guide**: "Screen for red flag symptoms"
2. **Agent autonomously executes**:
   - Calls `medical_db.check_conditions()`
   - Uses LLM to extract symptoms
   - Queries patient history
3. **Agent reports findings to guide**
4. **Guide makes protocol decision**:
   - Emergency escalation if red flags
   - Or continue to next step
5. **Repeat until complete**

---

## Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) - Local LLM runtime

### Setup

```bash
# 1. Install Ollama
brew install ollama  # macOS
# or visit ollama.com for other platforms

# 2. Download Gemma model (~2GB)
ollama pull gemma:2b

# 3. Install Python dependencies
cd medical-triage

# Option A: Using uv (recommended - avoids conflicts)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Option B: Using pip
pip install -r requirements.txt

# 4. Register the kernel with Jupyter (if using virtual environment)
python -m ipykernel install --user --name=medical-triage --display-name="Medical Triage (Python 3.11)"

# 5. Start Ollama server (in a separate terminal)
ollama serve
```

---

## Usage

### Run the Jupyter Notebook (Recommended)

```bash
# Start the notebook
jupyter notebook medical_triage_demo.ipynb
```

**Important:** When the notebook opens, select the **"Medical Triage (Python 3.11)"** kernel from the Kernel menu (Kernel → Change Kernel) to use the virtual environment with all dependencies.

Then execute cells one by one to see the agent-guide interaction.

### What You'll See

```
🚑 NEW PATIENT ARRIVAL

📋 Guide → Agent:
   Task: screen_red_flags
   Instructions: Check for emergency symptoms (mandatory protocol)

🤖 Agent executing...
   ✓ Called: medical_db.check_conditions()
   ✓ Analyzed patient statement with LLM
   ✓ Found: severe chest pain, cardiac history

📋 Guide decision:
   🚨 EMERGENCY ESCALATION
   Triage Level: IMMEDIATE
   Protocol: Emergency Cardiac Protocol

✅ Audit Trail:
   ✓ Red flag screening - completed
   ✓ Emergency protocol - activated
   ✓ All mandatory steps - followed
```

---

## Demo Scenarios

The notebook includes three scenarios:

### Scenario 1: Emergency (Red Flags)
- **Symptoms**: Severe chest pain
- **Guide Action**: Immediate escalation
- **Triage Level**: Level 1 - Immediate
- **Result**: Emergency Department NOW

### Scenario 2: Urgent (Critical Vitals)
- **Symptoms**: Moderate chest pain
- **Vitals**: BP 180/110, HR 120 (critical)
- **Guide Action**: All protocol steps, then urgent escalation
- **Triage Level**: Level 2 - Emergency

### Scenario 3: Non-Urgent (Routine)
- **Symptoms**: Minor issue
- **Vitals**: Normal
- **Guide Action**: Complete triage, standard recommendation
- **Triage Level**: Level 5 - Non-urgent

---

## File Structure

```
medical-triage/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── triage_guide.py              # Guide state machine (core pattern)
├── fake_tools.py                # Mock medical tools
└── medical_triage_demo.ipynb    # Interactive demo
```

---

## Key Components

### 1. Triage Guide (`triage_guide.py`)

The workflow controller - implements clinical protocol:

```python
class MedicalTriageGuide:
    """
    State machine that enforces medical triage protocol.
    
    States:
    - RED_FLAG_SCREENING (mandatory, can't skip)
    - CHIEF_COMPLAINT
    - MEDICAL_HISTORY  
    - VITAL_SIGNS (mandatory)
    - SEVERITY_ASSESSMENT
    - COMPLETE
    """
```

**Protocol enforcement:**
- Red flags screened first (always)
- Emergency escalation (if red flags detected)
- Vital signs required (mandatory step)
- Complete audit trail (every step logged)

### 2. Autonomous Agent (in notebook)

The execution engine - decides HOW to accomplish tasks:

```python
class SimpleMedicalAgent:
    def execute_task(self, task, instructions):
        """
        Agent autonomously:
        1. Interprets task
        2. Calls appropriate tools
        3. Processes results
        4. Reports back to guide
        """
```

**Agent autonomy:**
- Chooses which tools to call
- Decides how to query data
- Uses LLM for reasoning (optional)
- Compiles comprehensive reports

### 3. Fake Medical Tools (`fake_tools.py`)

Simulated medical systems:

```python
class MedicalDatabase:
    """Simulates patient records database"""
    def check_conditions(symptoms): ...

class VitalsMonitor:
    """Simulates vital signs monitoring"""
    def get_vitals(patient_id): ...
```

---

## Extending This Demo

To adapt this for real medical systems, you would need:

- **Clinical validation** by medical professionals
- **Real medical logic** (validated triage algorithms like ESI/CTAS, clinical NLP)
- **EMR/EHR integration** (FHIR APIs, secure patient data)
- **Regulatory compliance** (HIPAA, FDA)
- **Security** (authentication, encryption, access controls)
- **Persistent audit logs** and compliance reporting

---

## Troubleshooting

### "Ollama connection error"

```bash
# Make sure Ollama is running
ollama serve

# In another terminal
ollama list  # Check if gemma:2b is installed
```

### "Module not found"

```bash
# Install dependencies
pip install -r requirements.txt
```

### "Notebook not starting"

```bash
# Try reinstalling jupyter
pip install --upgrade jupyter notebook
jupyter notebook medical_triage_demo.ipynb
```

---

## Learn More

- **[Tool-as-Guide Pattern](../../README.md)** - Full pattern documentation, comparisons, and use cases
- **[Pizza Ordering Example](../01-pizza-ordering/)** - See the pattern with a chat interface

---

## License

MIT License

---

**Built to demonstrate reliable AI for critical systems** 🏥

