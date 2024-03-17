# Dodone

Dodone is a FastAPI based web application that provides a RESTful API for managing tasks.

## Table of Contents

- [Dodone](#dodone)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Testing](#testing)
  - [License](#license)

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. You can install the project dependencies with:

```sh
poetry install
```

## Usage

To run the application, use the following command:

```sh
uvicorn app.main:app --reload
```

## Project Structure

Here is a brief overview of the project's structure:

```plaintext
app/
    __init__.py
    api/
        __init__.py
        deps.py
        main.py
        routes/
            __init__.py
            login.py
            todos.py
            users.py
            utils.py
    core/
        __init__.py
        config.py
        crud.py
        db.py
        security.py
    crud.py
    main.py
    models.py
    utils.py
tests/
    __init__.py
```

## Testing

To run the tests, use the following command:

```sh
pytest
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.
