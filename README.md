# Mercury
Flexible, scalable financial data ingestion, storage, and service 

## Quick Start Guide for Project Setup

### 1. Setting Up the Environment:

**a.** Navigate to your project directory:

```bash
cd <root>/Mercury
```

**b.** Install Python version and select the version to use in the project directory.

```bash
pipenv --python 3.10.12
```

**c.** Install the project dependencies (including development ones) and activate the virtual environment:

```bash
pipenv install --dev
pipenv shell
```

This will install all the necessary packages, including `pre-commit`.

**d.** For running and testing python code, select the Python interpreter set by Pipenv.
Such as for VSCode, use the interpreter similar to the one highlighted in the settings screenshot:

![Alt text](images/interpreter.png)

### 2. Installing Pre-Commit Hooks:

**a.** Once the packages are installed, set up the pre-commit hooks:

```bash
pre-commit install --hook-type pre-commit --hook-type pre-push
```

With these commands, you've added hooks that will run both before committing (`pre-commit`) and before pushing (`pre-push`) to your version control.

### 3. Installing New Packages in Pipenv:

**a.** You can install new packages in pipenv by using the below command

```bash
pipenv install package_name==version --dev
```
Where package_name is your package that you want to install and the version is the specific version number of the package.

### 4. Workflow:

**a.** **Pre-Commit:** When you commit changes, the following scripts will be executed:

- YAML syntax check (`check-yaml`)
- Fix any files that don't end in a newline (`end-of-file-fixer`)
- Remove trailing whitespace from lines (`trailing-whitespace`)
- Organize your imports (`isort`)
- Format your Python code (`black`)
- Lint your Python code for errors and warnings (`pylint`)

_Note:_ If any of these checks fail, your commit will be blocked. This ensures that the committed code adheres to the project's quality standards.

**b.** **Pre-Push:** Before you push your changes, the following checks will be executed:

- Type checking of your Python code (`mypy`)
- Running the test suite with coverage (`pytest-check`)

If the tests fail, the push will be blocked. This ensures that only code passing the tests makes its way to the shared repository.


**Pushing Without Tests:** If you ever need to bypass the pre-push hooks (NOT recommended without a good reason), you can use `git push --no-verify`.