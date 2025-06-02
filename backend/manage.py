#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

import debugpy


def main():
    if os.environ.get("RUN_MAIN") == "true":
        try:
            debugpy.listen(("0.0.0.0", 5678))
            print("🚀 Debugger aguardando conexão na porta 5678 (não bloqueante)")
        except Exception as e:
            print(f"⚠️ Debugpy já em execução ou erro: {e}")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
