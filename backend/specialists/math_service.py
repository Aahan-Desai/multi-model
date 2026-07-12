from __future__ import annotations

import re

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.infrastructure.execution.python_executor import PythonExecutor
from backend.infrastructure.llm.chat_service import ChatService

logger = get_logger(__name__)


class MathService:
    """
    Specialist responsible for deterministic mathematical problem solving.

    Workflow:
        1. Generate Python code from the user's request.
        2. Execute the code deterministically.
        3. Generate a human-readable explanation from the execution result.
    """

    _CODE_GENERATION_PROMPT = """
You are an expert Python programmer.

Your task is to solve the user's mathematical request by writing Python code.

Rules:
- Return ONLY executable Python code.
- Do not use Markdown.
- Do not wrap the code in backticks.
- Do not include explanations or comments unless required for execution.
- Print the final answer using print().
"""

    _EXPLANATION_PROMPT = """
You are a mathematical assistant.

The computation has already been executed correctly.

Using the user's original question and the execution output,
provide a concise, clear explanation of the result.

Do not recompute anything.
Trust the execution output.
"""

    def __init__(
        self,
        chat_service: ChatService | None = None,
        python_executor: PythonExecutor | None = None,
    ) -> None:
        self._chat_service = chat_service or ChatService()
        self._python_executor = python_executor or PythonExecutor()

    def solve(self, query: str) -> str:
        """
        Solve a mathematical request deterministically.

        Args:
            query: User's mathematical request.

        Returns:
            A human-readable explanation of the computed result.

        Raises:
            RuntimeError:
                If code generation or execution fails.
            TimeoutError:
                If execution exceeds the configured timeout.
        """
        logger.info("Processing mathematical request.")

        code = self._generate_code(query)

        execution_result = self._python_executor.execute(code)

        return self._explain_result(
            query=query,
            execution_output=execution_result.stdout.strip(),
        )

    def _generate_code(self, query: str) -> str:
        """
        Generate executable Python code for the mathematical request.
        """
        response = self._chat_service.generate(
            model=settings.rag_model,
            system_prompt=self._CODE_GENERATION_PROMPT,
            user_prompt=query,
        )

        return self._extract_code(response)

    def _explain_result(
        self,
        query: str,
        execution_output: str,
    ) -> str:
        """
        Convert deterministic execution output into a natural-language explanation.
        """
        prompt = (
            f"User Question:\n{query}\n\n"
            f"Execution Output:\n{execution_output}"
        )

        return self._chat_service.generate(
            model=settings.rag_model,
            system_prompt=self._EXPLANATION_PROMPT,
            user_prompt=prompt,
        )

    @staticmethod
    def _extract_code(response: str) -> str:
        """
        Extract executable Python code from the LLM response.

        Supports both plain Python responses and fenced code blocks.
        """
        pattern = r"```(?:python)?\s*(.*?)```"
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(1).strip()

        return response.strip()