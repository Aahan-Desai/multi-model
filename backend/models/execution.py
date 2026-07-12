from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionResult:
    """
    Represents the outcome of executing a Python script.

    Attributes:
        stdout: Standard output produced during execution.
        stderr: Standard error produced during execution.
        return_code: Exit code returned by the Python process.
    """

    stdout: str
    stderr: str
    return_code: int