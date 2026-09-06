"""Шаг 70: канбан-доска."""

from .constants import SEEDED_STATUS_NAME, SEEDED_TASK_TITLE, SEEDED_USER_EMAIL

ALT_STATUS_NAME = "To Review"


def test_board_shows_columns_and_cards(tasks_page):
    """На доске видны и колонки статусов, и карточки задач."""
    tasks_page.open_board()
    titles = tasks_page.visible_column_titles()
    assert SEEDED_STATUS_NAME in titles, f"Колонки статусов не отрисованы: {titles}"
    assert len(tasks_page.visible_cards()) > 0, "На доске нет ни одной карточки"
    assert tasks_page.text_stays_visible(SEEDED_TASK_TITLE, "div"), "Карточки не держатся"


def test_create_task_shows_card_in_column(tasks_page, unique):
    title = f"Task-{unique}"
    tasks_page.create(title, "Проверка создания", SEEDED_USER_EMAIL, SEEDED_STATUS_NAME)
    tasks_page.open_board()
    assert tasks_page.card_is_in_column(title, SEEDED_STATUS_NAME)


def test_edit_task_updates_card(tasks_page, unique):
    new_title = f"Task-{unique}-updated"
    tasks_page.edit(SEEDED_TASK_TITLE, new_title=new_title)
    tasks_page.open_board()
    assert tasks_page.card_is_visible(new_title)


def test_change_status_moves_card(tasks_page, unique):
    title = f"Task-{unique}"
    tasks_page.create(title, "Проверка переноса", SEEDED_USER_EMAIL, SEEDED_STATUS_NAME)
    tasks_page.edit(title, new_status=ALT_STATUS_NAME)
    tasks_page.open_board()
    assert tasks_page.card_is_in_column(title, ALT_STATUS_NAME)
    assert not tasks_page.card_is_in_column(title, SEEDED_STATUS_NAME)


def test_filter_by_status_narrows_board(tasks_page):
    tasks_page.open_board()
    total = len(tasks_page.visible_cards())
    tasks_page.filter_by_status(SEEDED_STATUS_NAME)
    filtered = tasks_page.wait_for_card_count_change(total)
    assert 0 < filtered < total, f"Фильтр не сузил выдачу: было {total}, стало {filtered}"


def test_task_details_show_content(tasks_page, unique):
    title = f"Task-{unique}"
    content = f"Content-{unique}"
    tasks_page.create(title, content, SEEDED_USER_EMAIL, SEEDED_STATUS_NAME)
    tasks_page.open_details(title)
    assert tasks_page.has_visible_text(title)
    assert tasks_page.has_visible_text(content)
