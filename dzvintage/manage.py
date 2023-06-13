#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from telegram import Bot
from django.conf import settings


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dzvintage.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    # bot.set_webhook(settings.TELEGRAM_BOT_WEBHOOK_URL)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
