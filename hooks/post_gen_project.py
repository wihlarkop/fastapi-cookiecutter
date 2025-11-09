#!/usr/bin/env python
"""Post-generation hook to clean up the generated project based on cookiecutter choices."""

import os
import shutil


def remove_file(filepath):
    """Remove a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Removed: {filepath}")


def remove_dir(dirpath):
    """Remove a directory if it exists."""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
        print(f"Removed directory: {dirpath}")


def main():
    """Clean up files based on cookiecutter configuration."""

    # Get cookiecutter variables
    use_alembic = "{{ cookiecutter.use_alembic }}"
    use_docker = "{{ cookiecutter.use_docker }}"
    include_testing = "{{ cookiecutter.include_testing }}"
    include_external_integrations = "{{ cookiecutter.include_external_integrations }}"
    use_database = "{{ cookiecutter.use_database }}"

    # Remove Alembic files if not using Alembic
    if use_alembic == "no" or use_database == "no":
        remove_file("alembic.ini")
        remove_dir("migrations")
        print("Alembic configuration removed (not needed)")

    # Remove Docker files if not using Docker
    if use_docker == "no":
        remove_file("Dockerfile")
        remove_file(".dockerignore")
        print("Docker configuration removed (not needed)")

    # Remove test directory if not including tests
    if include_testing == "no":
        remove_dir("test")
        print("Test directory removed (not needed)")

    # Remove integrations folder if not needed
    if include_external_integrations == "no":
        remove_dir("src/integrations")
        print("Integrations directory removed (not needed)")

    # Remove health endpoint if not needed
    include_health_check = "{{ cookiecutter.include_health_check }}"
    if include_health_check == "no":
        remove_file("src/controllers/health.py")
        remove_file("src/schemas/health.py")
        print("Health endpoint files removed (not needed)")

    # Remove JWT files if not needed
    use_jwt = "{{ cookiecutter.use_jwt }}"
    if use_jwt == "no":
        remove_file("src/helper/jwt_token.py")
        remove_file("src/exceptions/jwt_token.py")
        print("JWT helper files removed (not needed)")

    # Remove authentication files if not needed
    include_authentication = "{{ cookiecutter.include_authentication }}"
    if include_authentication == "no":
        remove_file("src/models/user.py")
        remove_file("src/entities/user.py")
        remove_file("src/schemas/auth.py")
        remove_file("src/repositories/user.py")
        remove_file("src/services/auth.py")
        remove_file("src/controllers/auth.py")
        remove_file("src/dependencies/auth.py")
        remove_file("src/exceptions/auth.py")
        remove_file("src/helper/password.py")
        print("Authentication files removed (not needed)")

    print("\nProject generation completed successfully!")
    print(f"Project created at: {os.getcwd()}")


if __name__ == "__main__":
    main()
