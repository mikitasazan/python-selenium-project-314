APP_IMAGE ?= hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app
APP_CONTAINER ?= kanban-board
APP_PORT ?= 5173
APP_BASE_URL ?= http://127.0.0.1:$(APP_PORT)

.PHONY: install start stop restart test lint

install:
	uv sync

start:
	docker run --rm --name $(APP_CONTAINER) -p $(APP_PORT):5173 $(APP_IMAGE)

stop:
	- docker stop $(APP_CONTAINER)

restart: stop start

test:
	APP_BASE_URL=$(APP_BASE_URL) uv run pytest

lint:
	uv run ruff check .
