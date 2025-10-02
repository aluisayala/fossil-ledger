
# Contributing to Fossil-Ledger

Thank you for considering a contribution to **Fossil-Ledger**!  
This project is part of the OPHI symbolic cognition framework, which means every contribution must align with our **audit-ready, privacy-first, fossilization principles**.

---

## 📌 How to Contribute
- Open an [issue](../../issues) to propose features, report bugs, or ask questions.
- Fork the repository and create a feature branch for your changes.
- Submit a Pull Request (PR) with:
  - A clear description of the change.
  - Reference to any related issues.
  - Evidence that your contribution passes validation.

---

## ✅ Requirements for Acceptable Contributions
- **Coding Standard**
  - Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
  - Use [Conventional Commits](https://www.conventionalcommits.org) for commit messages.
- **Testing**
  - All new features and bug fixes must include tests.
  - Run `pytest` before submitting PRs to confirm no regressions.
- **Validation**
  - Code should respect the SE44 gate:  
    - Coherence (C) ≥ 0.985  
    - Entropy (S) ≤ 0.01  
    - RMS Drift ≤ 0.0011
- **Licensing**
  - Contributions must be compatible with the project license (Apache-2.0).
  - Do not introduce dependencies with restrictive or non-open licenses.

---

## 🛠️ Development Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourname/fossil-ledger.git
   cd fossil-ledger


Install dependencies:

pip install -r requirements.txt


Run tests:

pytest

🤝 Code of Conduct

By contributing, you agree to follow our Code of Conduct
.

🔐 Fossil Principle

All contributions must preserve the principle:
“Symbolic memory is not written. It is fossilized.”
