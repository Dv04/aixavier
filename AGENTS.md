# Repository Guidelines

This repository is being scaffolded for a collection of automation agents and supporting orchestration utilities. Follow the practices below so that early contributions converge toward a consistent, maintainable layout.

## Project Structure & Module Organization
- Keep runtime code in `src/aixavier/`, grouping agents under `src/aixavier/agents/` and shared abstractions under `src/aixavier/core/`.
- Detector runtimes temporarily live under `src/runners/` (`detectors.py` hosts the shared inference loop); plan to relocate to `src/aixavier/vision/` during the refactor.
- Place evaluation data, prompt templates, and fixtures in `assets/` with subfolders such as `assets/prompts/` and `assets/datasets/`.
- Store documentation artifacts in `docs/` and diagrams in `docs/diagrams/`.
- Co-locate smoke scripts or notebooks in `experiments/` but promote anything reusable into `src/`.
- House all automated tests in `tests/`, mirroring the `src/` package layout (e.g., `tests/agents/test_memory.py` exercises `src/aixavier/agents/memory.py`).

## Build, Test, and Development Commands
```bash
python -m venv .venv && source .venv/bin/activate      # bootstrap local environment
pip install -r requirements.txt                        # install core runtime deps
pip install -r requirements-dev.txt                    # install lint/test tooling
pytest                                                  # run the full unit and integration suite
ruff check src tests                                    # lint and static analysis
python -m build                                         # produce a distributable wheel/sdist
```

## Coding Style & Naming Conventions
- Use 4-space indentation, type hints, and Python 3.11+ features where they clarify intent.
- Run `black` (line length 100) and `ruff` before opening a pull request; configure editors to respect `.editorconfig`.
- Modules follow snake_case (`memory_router.py`), classes use PascalCase (`MemoryRouter`), and functions/variables use snake_case (`route_message`).
- Environment variables should be upper-case with underscores (`AGENT_TIMEOUT_SECONDS`) and defined in `.env.example`.
- When wiring detectors, ensure ONNX exports are staged under `models/<modality>/onnx/` for CPU validation and TensorRT engines under `models/usecases/<use-case>/` before enabling CI.
- Tracker utilities live in `src/trackers/bytetrack.py`; extend `SimpleTracker` or swap to full ByteTrack/ReID before productionization.

## Testing Guidelines
- Prefer `pytest` test modules named `test_<subject>.py`; within each module, describe behaviors (`def test_memory_router_retries_on_timeout():`).
- Add integration tests under `tests/integration/` when exercising external services or orchestrations.
- Target ≥90% coverage on critical agent pathways; update `tests/README.md` with edge cases when introducing new tooling.
- Use `pytest -k "<keyword>"` locally for focused runs and ensure CI passes before requesting review.
- Detector post-process tests require NumPy; export `AIXAVIER_ENABLE_NUMPY_TESTS=1` when the runtime is available.

## Commit & Pull Request Guidelines
- Adopt Conventional Commits from the outset (`feat: add planner agent skeleton`, `fix: tighten retry budget`); keep subject lines ≤72 characters.
- Squash work-in-progress commits locally; each PR should read as a cohesive story with linked issues or roadmap items.
- Pull requests must include: scope summary, testing notes (commands + results), screenshots or logs for UI/UX changes, and follow-up tasks if applicable.
- Tag reviewers responsible for the touched subsystem (`@agents`, `@infra`) and add TODOs to `docs/roadmap.md` instead of burying them in code comments.

## Security & Configuration Tips
- Never commit API keys or secrets; rely on `.env` (gitignored) and document required keys in `.env.example`.
- Rotate credentials quarterly and reference secret names (not values) in documentation.
- When integrating third-party tools, sandbox them under dedicated service accounts and capture onboarding steps in `docs/integrations/`.
