def test_add_category_with_and_without_budget(monkeypatch, tmp_path):
    from src.persistence import storage
    storage.DEFAULT_DATA_FILE = tmp_path / "budget_state.json"

    from src.agent.chat import BudgetChatAgent

    agent = BudgetChatAgent()

    # Without budget
    out = agent.handle("create category Utilities")
    assert "Added category Utilities" in out or "Set Utilities" in out

    # With budget
    out = agent.handle("add category Travel to $300")
    assert "Set Travel" in out and "$300.00" in out

    summary = agent.handle("summary")
    assert "Utilities" in summary
    assert "Travel" in summary
