"""Значения, общие для всех тестов."""

import os

LOGGER_NAME = "kanban.tests"

# Бэкенда у приложения нет: логин и пароль подходят любые.
CREDENTIALS = {"username": "qa-engineer", "password": "secret"}

DEFAULT_TIMEOUT = int(os.getenv("SELENIUM_DEFAULT_TIMEOUT", "10"))

# Текст на дашборде. Он появляется только после успешного входа и лежит внутри
# `main`, поэтому годится как признак того, что за формой входа что-то есть.
DASHBOARD_TEXT = "Lorem ipsum sic dolor amet..."

# Записи, с которыми приложение стартует. Их видно на списках без подготовки.
SEEDED_USER_EMAIL = "john@google.com"
SEEDED_STATUS_NAME = "Draft"
SEEDED_LABEL_NAME = "bug"
SEEDED_TASK_TITLE = "Task 1"
SEEDED_USERS_COUNT = 8
SEEDED_STATUSES_COUNT = 5
SEEDED_LABELS_COUNT = 5
