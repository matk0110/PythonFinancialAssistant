import pytest


def test_chat_auto_categorize_groceries_to_food(monkeypatch, tmp_path):
    # isolate storage path by monkeypatching DEFAULT_DATA_FILE
    from src.persistence import storage
    storage.DEFAULT_DATA_FILE = tmp_path / "budget_state.json"

    from src.agent.chat import BudgetChatAgent

    agent = BudgetChatAgent()
    assert "Set Food" in agent.handle("set Food to $100")

    # User doesn't name the exact category, uses a description instead
    msg = agent.handle("spent 30 on groceries")
    assert "Food" in msg
    assert "auto-categorized" in msg

    # Verify it affected the Food bucket
    summary = agent.handle("summary")
    assert "Food" in summary
    # Should reflect 30 spent out of 100
    assert "$30.00" in summary or "30.00" in summary
