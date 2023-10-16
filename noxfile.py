"""Nox sessions."""
import os
import shlex
import shutil
import sys
from pathlib import Path
from textwrap import dedent
from typing import Optional

import nox
from nox_poetry import Session, session

package = "configclasses"
python_versions = ["3.11", "3.10", "3.9", "3.12"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    "safety",
    "tests",
)


@session(python=python_versions[0])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@session
@nox.parametrize(
    "python,poetry",
    [(python_versions[0], "1.0.10"), *((python, None) for python in python_versions)],
)
def tests(session: Session, poetry: Optional[str]) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(
        "coverage[toml]",
        "poetry",
        "pytest",
        "pytest-datadir",
        "pygments",
        "typing_extensions",
    )

    if poetry is not None:
        session.run_always(
            "python", "-m", "pip", "install", f"poetry=={poetry}", silent=True
        )

    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session(python=python_versions[0])
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(python=python_versions)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    session.install(".")
    session.install("pytest", "typeguard", "pygments")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)