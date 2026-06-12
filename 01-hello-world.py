import asyncio
from google.antigravity import Agent, LocalAgentConfig

async def main():
    # Initialize LocalAgentConfig
    # Configuration for the local harness backend
    config = LocalAgentConfig(
        model="gemini-3.1-flash-lite",
    )
    # Create an agent
    async with Agent(config) as root_agent:
        # Invoke Chat, get response
        response = await root_agent.chat(
            "How many files are in the current directory?")
        # Print result
        result = await response.text()
        print(result)


async def run():
    await main()

if __name__ == "__main__":
    asyncio.run(run())
