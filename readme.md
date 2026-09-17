# Autonomous Cognitive Debugging Memory Architecture

Status: In active development

## Overview

This project is a brain-driven debugging system for Python applications, built around an agentic orchestration layer that combines retrieval, reasoning, and execution context to diagnose software issues more intelligently than a passive static analyzer.

At the center of the system is the Brain — a memory-aware control layer that coordinates short-term task execution, persistent knowledge, and contextual understanding across debugging sessions. The Brain is designed to manage state, prioritize work, retain relevant facts, and support iterative reasoning over time.

The broader system integrates repository indexing, retrieval-augmented context gathering, and large-language-model prompting to support error analysis, root-cause investigation, and fix generation in real-world Python projects, especially Django and Flask applications.

## Core Idea: The Brain

The Brain is the project’s central intelligence layer.

It is responsible for:

- tracking active tasks and debugging work in short-term memory
- maintaining session context and evolving project understanding
- persisting useful facts and recurring patterns in long-term memory
- coordinating task execution and state transitions across an investigation cycle
- enabling an agentic workflow that can reason over code, tests, symptoms, and fixes

This design is intended to move beyond simple prompt-response tools toward a more memory-augmented, stateful debugging agent that behaves more like an internal reasoning engine than a one-shot assistant.

## Objectives

- Build a debugging agent that can reason over repository context, failing tests, and execution signals.
- Create a memory architecture that supports both real-time task management and long-term knowledge retention.
- Reduce debugging latency by surfacing the most relevant code and diagnostic artifacts first.
- Enable a structured loop of investigation, hypothesis formation, fix proposal, and validation.
- Provide support for Python web frameworks commonly used in production environments, including Django and Flask.

## Key Technical Features

- Agentic multi-step orchestration for diagnosis and mitigation workflows
- Retrieval-augmented context using indexed source files, tests, and documentation
- Brain-based memory model with short-term execution state and long-term fact retention
- Task lifecycle management for actionable debugging work
- Framework-aware analysis for Django and Flask project structures
- LLM integration for reasoning, explanation generation, and patch suggestion
- Configurable vector-store and model backend
- CLI and programmatic interfaces for interactive or automated debugging flows

## High-Level Architecture

- Brain layer: central memory and orchestration logic; manages active tasks, context, and persistent knowledge
- Memory system:
  - Short-term memory: volatile runtime state, task queue, current session context
  - Long-term memory: persistent facts, patterns, and contextual knowledge across runs
- Retrieval layer: indexes code, docs, and tests and retrieves relevant snippets based on error states or queries
- Orchestrator / agent: coordinates reasoning steps, diagnostic prompts, and validation loops
- LLM backend: configurable provider for generation and embeddings
- Tooling integration: pytest, static analysis, and runtime instrumentation signals

## Brain Memory Model

The project uses a layered memory design inspired by agentic systems:

- Short-term memory stores active objectives, open tasks, and transient session state.
- Long-term memory retains durable facts that may help future debugging sessions.
- Context updates enable incremental accumulation of understanding rather than stateless prompting.
- Task tracking allows the system to maintain a queue of work, mark completions, and preserve operational continuity.

This is one of the most important differentiators of the project: the ability to reason with memory instead of treating each interaction as isolated context.

## Supported Frameworks

- Django
- Flask

The architecture is designed to support additional Python frameworks through modular inspection and prompting components.

## Getting Started

### Prerequisites

- Python 3.8+ (3.10+ recommended)
- Virtual environment tooling such as venv, pipenv, or poetry
- Access to an LLM provider and API key if using a hosted model

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Akinfiresoye-Victor/agentic_python_debugger.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Keep secrets out of source control and store them in a `.env` file or a secure platform secret manager.

Example configuration:

```env
# .env (example)
OPENAI_API_KEY=sk-xxx
LLM_MODEL=gpt-4o
EMBEDDINGS_MODEL=text-embedding-3
VECTOR_STORE_PATH=./vectorstore
DATABASE_URL=sqlite:///dev.db
LOG_LEVEL=INFO
```

If you are using a hosted vector database such as Pinecone, Weaviate, or Milvus, configure the appropriate connection parameters instead of relying on a local vector store path.

## Usage

### Interactive debugging workflow

Run the system through the project entry point:

```bash
python -m agentic_debugger.cli
```

or:

```bash
python main.py --project-path /path/to/project --mode analyze --target-file path/to/file.py
```

### Analyze a failing test

1. Reproduce the error locally:
   ```bash
   pytest tests/my_test.py::test_something -q
   ```
2. Pass the failing test or stack trace to the agent for contextual analysis and remediation guidance.

### Generate a patch

1. The Brain retrieves relevant repository context and failure metadata.
2. The agent synthesizes an explanation and candidate fix.
3. The developer reviews the proposed patch and applies it to the codebase.

## Running Tests

If the project includes automated tests, run the suite with:

```bash
pytest -q
```

New modules or behavioral changes should include focused tests for memory flow, retrieval logic, orchestration behavior, and integration boundaries.

## Development Notes

Suggested project structure:

```text
agentic_debugger/
├── cli.py                # CLI entry point
├── core/                 # Orchestration and reasoning logic
├── brain/                # Memory model, task queue, and context state
├── retriever/            # Indexing, embeddings, and vector search
├── integrations/         # Django and Flask framework helpers
├── tests/                # Automated validation
├── requirements.txt
├── README.md
```

- Use structured logging for observability and debugging.
- Keep prompt templates isolated for cleaner experimentation and tuning.
- Maintain clear boundaries between retrieval, reasoning, memory, and execution layers.
- Treat the Brain as the primary architectural abstraction around which the agent is built.

## Contributing

- Open an issue to discuss major architectural or feature changes before implementation.
- Fork the repository and submit a pull request for review.
- Follow the existing coding standards and include tests for new functionality.
- Document configuration and usage changes when introducing new modules or capabilities.

## Roadmap

- Core memory and orchestration improvements for the Brain
- Deeper Django and Flask inspection capabilities
- Stronger retrieval pipelines and code-context ranking
- End-to-end validation workflows for bug reproduction and fix verification
- Improved CLI and developer tooling for interactive debugging sessions

## Security and Configuration

- Do not commit secrets such as API keys or credentials.
- Use `.env` files or a secure secret manager for sensitive values.
- Sanitize source code and environment content before sending it to third-party LLM providers when privacy is a concern.

## License

No license has been specified yet. Consider adding a LICENSE file such as MIT or Apache-2.0 if you intend to support wider public use and contributions.

## Contact

- Repository: https://github.com/Akinfiresoye-Victor/agentic_python_debugger
- For feature requests, bug reports, or collaboration, open an issue in the repository.

## References

- Retrieval-augmented generation (RAG)
- Agentic memory systems and stateful reasoning architectures
- LLM prompt engineering and tool-augmented workflows
- Python testing, linting, and validation tooling such as pytest, flake8, and mypy
