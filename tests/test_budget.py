import pytest
from src.budget.model import Budget


def test_set_and_spend():
    b = Budget()
    b.set_category('Food', 100)
    b.add_spend('Food', 25)
    assert b.remaining('Food') == 75


def test_unknown_category():
    b = Budget()
    with pytest.raises(ValueError):
        b.add_spend('Nope', 10)


def test_chat_agent_basic(monkeypatch, tmp_path):
    # isolate storage path by monkeypatching DEFAULT_DATA_FILE
    from src.persistence import storage
    storage.DEFAULT_DATA_FILE = tmp_path / "budget_state.json"
    from src.agent.chat import BudgetChatAgent
    agent = BudgetChatAgent()
    assert "No categories" in agent.handle("summary")
    assert "Set Food" in agent.handle("set Food to $200")
    assert "Added" in agent.handle("spent $50 on food")
    out = agent.handle("summary")
    assert "Food" in out and "%" in out
