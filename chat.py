from src.agent.chat import BudgetChatAgent


def main():
    agent = BudgetChatAgent()
    print("Chat Budget Agent (type 'help' for commands, 'quit' to exit)")
    while True:
        try:
            user = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        resp = agent.handle(user)
        print(resp)
        if resp.strip().lower() == "goodbye.":
            break


if __name__ == "__main__":
    main()
