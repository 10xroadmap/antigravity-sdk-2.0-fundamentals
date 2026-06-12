import asyncio
from google.antigravity import Agent
from google.antigravity import LocalAgentConfig
from google.antigravity import types
from google.antigravity.hooks import policy
import pydantic


class RunCommandArgs(pydantic.BaseModel):
    """Arguments for run_command tool."""
    command_line: str

def block_delete_operation(input: RunCommandArgs) -> bool:
    """if 'rm' in command line arguments, block"""
    return "rm" in input.command_line


async def main() -> None:
    policies = [
        # 1. Deny everything by default
        policy.deny_all(),
        # 2. Allow reading directory contents
        policy.allow(types.BuiltinTools.LIST_DIR.value),
        # 3. Allow running commands, but block dangerous 'rm' commands
        policy.allow(types.BuiltinTools.RUN_COMMAND.value),
        policy.deny(
            types.BuiltinTools.RUN_COMMAND.value,
            when=block_delete_operation,
            name="block-delete-operation",
        ),
    ]

    config = LocalAgentConfig(model="gemini-3.1-flash-lite", policies=policies)

    async with Agent(config) as root_agent:
        print("\n Starting chat ....")

        # # Try a safe command (should be allowed)
        prompt = "List the files in the current directory."
        print(f"\n  User: {prompt}")
        response = await root_agent.chat(prompt)
        print(f"  Agent: {await response.text()}")
        # Try a dangerous command (should be denied by policy)
        # prompt = "Delete all files using rm -rf"
        # print(f"\n  User: {prompt}")
        # response2 = await root_agent.chat(prompt)
        # print(f"  Agent: {await response2.text()}")


if __name__ == "__main__":
    asyncio.run(main())
