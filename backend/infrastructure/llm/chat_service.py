from __future__ import annotations

from openai import OpenAI

import json
from typing import Any

from backend.core.clients import get_groq_client
from backend.core.logging import get_logger
from backend.models.router_response import RouterResponse
from backend.models.tool_call import ToolCall

logger = get_logger(__name__)


class ChatService:
    """
    Service responsible for interacting with the Groq Chat Completions API.

    This class provides a provider-agnostic interface for generating chat
    responses. Higher-level modules should depend on this service rather than
    directly interacting with the Groq/OpenAI SDK.
    """

    def __init__(self, client: OpenAI | None = None) -> None:
        """
        Initialize the chat service.

        Args:
    model:
        Name of the Groq model to use.

    system_prompt:
        High-level instructions for the model.

    user_prompt:
        The user's actual prompt.

    temperature:
        Sampling temperature. Lower values produce more deterministic
        outputs.

    max_tokens:
        Optional maximum number of output tokens.
        """
        self._client = client or get_groq_client()

    def generate(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> str:
        """
        Generate a response from the configured Groq model.

        Args:
            system_prompt:
                High-level instructions for the model.

            user_prompt:
                The user's actual prompt.

            temperature:
                Sampling temperature. Lower values produce more deterministic
                outputs.

            max_tokens:
                Optional maximum number of output tokens.

        Returns:
            The generated response text.

        Raises:
            RuntimeError:
                If the model returns an empty response.

            Exception:
                Any exception raised by the Groq SDK is intentionally
                propagated to the caller.
        """

        logger.info("Generating chat completion using model '%s'.", model)

        try:
            response = self._client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                tool_choice="auto",
            )

            content = response.choices[0].message.content

            if not content:
                logger.error("Received an empty response from the LLM.")
                raise RuntimeError("LLM returned an empty response.")

            logger.debug("Successfully generated chat completion.")

            return content.strip()
        except Exception as exc:
            logger.exception("Error generating chat completion: %s", exc)
            raise 
        

    def generate_with_tools(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        tools: list[dict[str, Any]],
    ) -> RouterResponse:
        """
        Generate a response using tool calling.

        Args:
            model:
                Name of the model to use.

            system_prompt:
                High-level instructions for the model.

            user_prompt:
                The user's request.

            tools:
                Tool definitions available to the model.

        Returns:
            RouterResponse containing content and optionally a ToolCall.

        Raises:
            RuntimeError:
                If the model returns an invalid tool call.
        """

        logger.info(
            "Generating tool-aware completion using model '%s'.",
            model,
        )
        
        response = self._client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            tools=tools,
            tool_choice="required",
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return RouterResponse(content=message.content or "", tool_call=None)

        tool_call = message.tool_calls[0]

        try:
            arguments = json.loads(
                tool_call.function.arguments
            )
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Model returned invalid tool arguments."
            ) from exc

        return RouterResponse(
            content=message.content or "",
            tool_call=ToolCall(
                name=tool_call.function.name,
                arguments=arguments,
            ),
        )