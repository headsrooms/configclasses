import nox


@nox.session(python=["3.9", "3.10", "3.11", "3.12"])
def tests(session):
    args = session.posargs
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("pytest", *args)


@nox.session
def coverage(session):
    session.run("poetry", "install", "--with", "dev", external=True)
    try:
        session.run("coverage", "run", "-m", "pytest")
    finally:
        # Display coverage report even when tests fail.
        session.run("coverage", "report")
