from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.models.execution import ExecutionResult

logger = get_logger(__name__)


class PythonExecutor:
    """
    Executes Python code in an isolated subprocess.

    This class is responsible only for code execution. It does not generate
    code, interpret results, or perform any business logic.
    """

    def __init__(self, timeout: int | None = None) -> None:
        self._timeout = timeout or settings.python_execution_timeout

    def execute(self, code: str) -> ExecutionResult:
        """
        Execute Python code in a separate process.

        Args:
            code: Python source code to execute.

        Returns:
            ExecutionResult containing stdout, stderr, and the process exit code.

        Raises:
            ValueError:
                If the provided code is empty.

            TimeoutError:
                If execution exceeds the configured timeout.

            RuntimeError:
                If the execution process cannot be started.
        """
        if not code.strip():
            raise ValueError("Code cannot be empty.")

        logger.info("Executing Python code.")

        logger.debug("Generated code (%d characters).", len(code))

        temp_file_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8",
            ) as temp_file:
                temp_file_path = Path(temp_file.name)
                temp_file.write(code)
                temp_file.flush()

            completed = subprocess.run(
                [sys.executable, str(temp_file_path)],
                capture_output=True,
                text=True,
                timeout=self._timeout,
                check=False,
            )

            logger.info(
                "Python execution completed with exit code %d.",
                completed.returncode,
            )

            return ExecutionResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                return_code=completed.returncode,
            )

        except subprocess.TimeoutExpired as exc:
            logger.exception("Python execution timed out.")
            raise TimeoutError(
                f"Python execution exceeded {self._timeout} seconds."
            ) from exc

        except OSError as exc:
            logger.exception("Failed to start Python subprocess.")
            raise RuntimeError("Unable to execute Python code.") from exc

        finally:
            if temp_file_path is not None and temp_file_path.exists():
                try:
                    temp_file_path.unlink()
                except Exception as cleanup_exc:
                    logger.warning(
                        "Failed to remove temporary file %s: %s",
                        temp_file_path,
                        cleanup_exc,
                    )