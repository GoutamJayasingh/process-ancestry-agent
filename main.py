from agent.orchestrator import run_question


def main():
    print("=" * 55)
    print("  Process Tree & Ancestry Agent")
    print("  Powered by Groq + MCP")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 55)

    while True:
        try:
            question = input("\nYou: ").strip()

            if question.lower() in {"exit", "quit"}:
                print("Agent: Goodbye!")
                break

            if not question:
                continue

            print("\nAgent: Thinking...")
            answer = run_question(question)
            print(f"\nAgent: {answer}")

        except KeyboardInterrupt:
            print("\nAgent: Goodbye!")
            break
        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()
