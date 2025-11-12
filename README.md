# Tool-as-Guide

> An architectural pattern for building reliable, auditable AI agents by separating workflow control from execution

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 The Problem

**Autonomous AI agents are powerful but unreliable for critical workflows:**

- ❌ Skip important steps
- ❌ Inconsistent behavior across runs  
- ❌ Hard to audit or debug
- ❌ Can't guarantee protocol compliance
- ❌ Unsuitable for regulated domains

**Current solutions don't solve this:**
- **Prompts**: Too fragile ("please follow these steps...")
- **Traditional workflows**: LLM is passive, no agency
- **Agent frameworks**: Too unpredictable for critical systems

---

## 💡 The Solution: Tool-as-Guide Pattern

**Key insight:** What if the workflow engine is a *tool* that the LLM actively queries?

```mermaid
sequenceDiagram
    participant User
    participant LLM as LLM/Agent
    participant Guide as Workflow Guide (Tool)
    
    User->>LLM: "I need help with X"
    LLM->>Guide: guide.start_workflow()
    Guide-->>LLM: {instruction: "Do step 1", required_data: [...]}
    LLM->>User: Executes step 1
    User->>LLM: Provides response
    LLM->>Guide: guide.continue(session_id, response)
    Guide-->>LLM: {instruction: "Do step 2", validation: "passed"}
    LLM->>User: Executes step 2
    Note over LLM,Guide: LLM drives execution<br/>Guide enforces protocol
```

### How It Works

1. **LLM/Agent has autonomy** - Drives conversation, executes tasks, makes decisions
2. **Guide provides instructions** - What to do next, what data is needed, what validates
3. **Protocol is enforced** - Can't skip steps, consistent behavior, auditable trail

### 🗺️ Think of It Like GPS Navigation

When you're driving through a city:
- **You're the intelligent, capable driver** - You know how to navigate traffic, make decisions, handle unexpected situations
- **GPS provides turn-by-turn instructions** - It tells you which route to follow, which turn to take next
- **GPS doesn't drive for you** - But it ensures you don't miss critical turns or get lost

**Tool-as-Guide works the same way:**
- **Agent is the intelligent worker** - Capable of reasoning, adapting, executing tasks
- **Guide provides step-by-step instructions** - What to do next, what protocol to follow
- **Guide doesn't do the work** - But it ensures critical steps aren't skipped and protocols are followed

The agent stays intelligent and autonomous. The guide ensures reliability and compliance.

> **For the technically inclined:** The Tool-as-Guide pattern is a workflow engine with inversion of control, acting as a protocol-driven supervisor for agentic systems.

### The Architectural Inversion

```mermaid
graph TB
    subgraph "Traditional Workflow Engine"
        WE[Workflow Engine<br/>Controls Everything] -->|executes| L1[LLM<br/>Passive Task]
        L1 -->|returns| WE
    end
    
    subgraph "Agent Framework"
        A[LLM Agent<br/>Controls Everything] -->|calls| T[Tools<br/>Passive Utilities]
        T -->|returns| A
    end
    
    subgraph "Tool-as-Guide (Novel)"
        L2[LLM/Agent<br/>Active Driver] -->|queries| G[Guide Tool<br/>Workflow Engine]
        G -->|returns instructions| L2
        L2 -->|executes & reports| G
    end
    
    style L2 fill:#90EE90
    style G fill:#87CEEB
```

**Tool-as-Guide** combines the best of both:
- ✅ Agent autonomy (LLM drives interaction)
- ✅ Workflow reliability (Guide enforces protocol)

---

## 🎬 Live Examples

### 🍕 Pizza Ordering - Chat Interface

![Pizza Ordering Demo](examples/01-pizza-ordering/demo.gif)

A fun, approachable example showing the pattern with Claude Desktop:
- **Guide controls**: Order of questions (crust → category → toppings → size → confirm)
- **Claude executes**: Natural conversation, understands responses, relays questions
- **Result**: Consistent ordering flow, can't skip steps, great UX

[Try it yourself →](examples/01-pizza-ordering/)

---

### 🏥 Medical Triage - Autonomous Agent

![Medical Triage Demo](examples/02-medical-triage/demo.gif)

A serious example showing the pattern with autonomous agents:
- **Guide controls**: Clinical protocol (red flags → history → vitals → assessment)
- **Agent executes**: Calls medical databases, queries records, processes data
- **Result**: Protocol-compliant triage, emergency escalation, audit trail

[Try it yourself →](examples/02-medical-triage/)

---

### 🔧 cursor-extend - Coming Soon (Preview)

> **⚠️ PREVIEW**: Tool for generating Tool-as-Guide implementations in Cursor IDE
> 
> Coming soon! This will help developers quickly generate workflow guide tools.
> 
> Stay tuned for announcement.

---

## 📊 Example Comparison

| Aspect | Pizza Ordering | Medical Triage |
|--------|---------------|----------------|
| **Interface** | Chat (Claude Desktop) | Autonomous Agent (Jupyter) |
| **Use Case** | Low stakes, conversational | High stakes, critical system |
| **AI Role** | Relays messages to user | Executes tasks autonomously |
| **Guide Role** | Returns prompts/questions | Returns tasks & protocol decisions |
| **Tools Used** | State machine only | State machine + DB + Classifier + Monitor |
| **LLM** | Claude (cloud) | Gemma (local, open) |
| **Domain Knowledge** | In guide (menu, options) | Separate classifier tool |
| **Purpose** | Show pattern basics | Show pattern for autonomous agents |
| **Audit Trail** | Session states | Full protocol compliance log |

**Both demonstrate the same core pattern in different contexts**, showing its versatility from simple chatbots to critical autonomous systems.

---

## 🚀 Quick Start

Choose an example to explore:

### 🍕 [Pizza Ordering Example](examples/01-pizza-ordering/)
Chat interface demo with Claude Desktop or Cursor. Perfect for understanding the basics.

### 🏥 [Medical Triage Example](examples/02-medical-triage/)
Autonomous agent demo with Jupyter and local LLM. Shows the pattern for critical systems.

Each example includes complete setup instructions and usage guide.

---

## 🏗️ Pattern Architecture

### Key Principles

1. **Separation of Concerns**
   - Guide: WHAT to do (workflow logic, validation, protocol)
   - Agent: HOW to do it (execution, reasoning, tool calls)

2. **Inversion of Control**
   - Agent queries the guide (not controlled by it)
   - Guide returns instructions (not commands)

3. **Stateful Sessions**
   - Each workflow has a unique session
   - State persists across interactions
   - Audit trail is automatic

4. **Deterministic Protocols**
   - Workflow logic lives in code
   - Same input → same workflow
   - Testable, verifiable, compliant

5. **Progressive Disclosure**
   - Agent receives only current instruction
   - Next steps revealed when needed
   - Reduces context window, improves focus

---

## 📚 Documentation

All documentation is in the main README and individual example folders:

- **Pattern Overview** - You're reading it!
- **Pizza Ordering Example** - See `examples/01-pizza-ordering/README.md`
- **Medical Triage Example** - See `examples/02-medical-triage/README.md`

---

## 🌟 Use Cases

This pattern is particularly powerful for:

### Critical Systems
- 🏥 **Healthcare** - Enforce clinical protocols, emergency escalation
- 💰 **Finance** - Regulatory compliance, risk checks
- ⚖️ **Legal** - Document review checklists, thoroughness requirements

### Operational Workflows  
- 🚀 **Deployments** - Quality gates, approval workflows
- 🛡️ **Security** - Incident response protocols
- 📞 **Customer Support** - Troubleshooting procedures

### Any Domain Where:
- Protocol compliance is required
- Steps can't be skipped
- Behavior must be auditable
- Consistency matters more than flexibility

### Efficiency Benefits

Beyond reliability, this pattern also improves performance and reduces costs:

- **Smaller context windows**: Guide provides only the current instruction, not the entire workflow tree
- **Progressive disclosure**: Agent loads only what it needs at each step
- **Faster execution**: Deterministic protocol logic runs in the guide (not LLM inference)
- **Lower token costs**: Similar to Anthropic's [code execution research](https://www.anthropic.com/engineering/code-execution-with-mcp), processing logic outside the model reduces token consumption by 90%+

The guide acts as an efficient coordinator—the LLM only sees "what to do next," not "all possible paths."

---

## 🆚 How This Differs from Other Approaches

### 1. Prompt-Based Instructions (Fragile & Opaque)

Most LLM applications today rely on carefully crafted prompts ("think step by step...", "call tools as needed"). This approach is:

- **Brittle**: Minor prompt changes, model updates, or LLM randomness can produce different results
- **Opaque**: No clear audit trail—workflow logic is implicit in prompts and model reasoning
- **Unpredictable**: Can't guarantee every step will be followed in regulated processes

### 2. Traditional Workflow Engines (No LLM Intelligence)

Conventional workflow engines define steps externally but lack LLM adaptability:

- **Rigid**: The engine holds all logic—LLMs just fill in text generation
- **Limited Intelligence**: Little opportunity for adaptive reasoning
- **Separated**: Workflow and AI capabilities don't integrate well

### 3. Multi-Agent Supervision (Still Probabilistic)

Some architectures use supervising agents to check other agents' work. While this improves reliability:

- **Still LLM-driven**: Error correction is probabilistic, supervisors can miss violations
- **Weakly auditable**: Better than single-agent prompts, but no external testable flow
- **Complex**: Multiple LLMs increase cost and latency

### 4. Tool-as-Guide (Hybrid Approach)

The Tool-as-Guide pattern combines the strengths of both:

- **Deterministic Protocol**: Workflow state machine decides every step—LLM executes but doesn't decide
- **Context-Rich Guidance**: Tool provides detailed instructions, templates, and context for each step
- **True Auditability**: Code-based workflow with explicit state transitions
- **Debuggable**: Failures isolated to specific logic/data steps, not buried in prompts
- **LLM Intelligence**: Agent can still reason and adapt within the bounds of each step

**In essence:** The workflow is deterministic and auditable (like traditional engines), but the execution is intelligent and adaptive (like LLM agents).

---

## 🔧 Implementations

The pattern can be implemented with various technologies:

- ✅ **MCP (Model Context Protocol)** - Shown in examples
- 🔄 **LangGraph** - State machine framework
- 🔄 **Temporal** - Workflow engine  
- 🔄 **Custom** - Pure Python/JavaScript

**The pattern is technology-agnostic.** Choose the implementation that fits your stack.

---

## 🤝 Contributing

We welcome contributions! Especially:

- Additional example implementations
- Integration with other workflow engines
- Documentation improvements
- Use case descriptions

Open an issue or pull request to get started.

---

## 📜 License

MIT License

---

**Built with ❤️ to make AI reliable for critical systems**


