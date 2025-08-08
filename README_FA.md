
# Free Spending Budget Agent

## 🧠 Project Overview
This Python agent is designed to help financially inexperienced individuals set and track a free spending budget. It guides users through budgeting by category and allows them to monitor their spending using manual input or photo-based receipt tracking.

## 🎯 Goals & Success Criteria
- Help users set realistic free spending budgets
- Enable easy tracking of expenses by category
- Support photo-based receipt input
- Ensure users understand how much they have left to spend

## 👤 Target User
- Financially inexperienced individuals
- Prefer simple, guided experiences
- May not be tech-savvy

## ✨ Features
- Guided budget setup by spending categories
- Real-time tracking of remaining budget
- Manual input and photo-based receipt parsing
- Alerts when nearing budget limits
- Simple command-line interface (CLI) with future web interface support

## 🛠️ Tech Stack
- Python 3
- VS Code with GitHub Copilot (GPT-5)
- Pillow (image handling)
- pytesseract (OCR for receipts)
- pandas (data management)

## 🚀 Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/budget-agent.git
   cd budget-agent
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Usage Guide (Chat-only)
1. Start chat agent:
   ```bash
   python chat.py
   ```
2. Try commands:
   - `set Food to $200`
   - `spent $12.50 on Food`
   - `show summary`
   - `list categories`
   - `save` / `quit`

## 🔄 Development Workflow
- Use GitHub Copilot for code generation
- Track tasks in `tasks.md` or GitHub Issues
- Test modules individually before integration
- Maintain modular and reusable code

## 🌱 Future Enhancements
- Natural language input for spending entries
- Image classification for auto-categorization
- Web interface using Flask or Streamlit
- Budget insights and recommendations

## 📄 License
MIT License
