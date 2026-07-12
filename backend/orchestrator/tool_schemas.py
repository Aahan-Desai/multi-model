from __future__ import annotations

from typing import Final

TOOLS: Final = [
    {
        "type": "function",
        "function": {
            "name": "rag_search",
            "description": (
                "Answer questions using the indexed knowledge base through "
                "retrieval-augmented generation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The user's question.",
                    },
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vision_analysis",
            "description": (
                "Analyze an uploaded image or video and answer questions "
                "about its contents."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": (
                            "The user's request describing the desired analysis."
                        ),
                    },
                },
                "required": ["prompt"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search trusted web sources to answer questions requiring "
                "current or external information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query.",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "solve_math",
            "description": (
                "Solve mathematical or computational problems using "
                "deterministic Python execution."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "The mathematical problem to solve.",
                    },
                },
                "required": ["problem"],
                "additionalProperties": False,
            },
        },
    },
]