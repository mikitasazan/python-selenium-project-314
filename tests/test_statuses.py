"""Шаг 50: раздел «Статусы»."""

from .constants import SEEDED_STATUS_NAME, SEEDED_STATUSES_COUNT


def test_status_list_shows_records(statuses_page):
    statuses_page.open_list()
    for header in ("Name", "Slug"):
        assert statuses_page.has_visible_text(header, "span"), f"Нет колонки {header}"
    assert statuses_page.text_stays_visible(SEEDED_STATUS_NAME, "td"), "Строки списка не держатся"
    assert len(statuses_page.visible_rows()) == SEEDED_STATUSES_COUNT


def test_create_status_adds_row(statuses_page, unique):
    name = f"Review {unique}"
    statuses_page.create(name, f"review-{unique}")
    statuses_page.open_list()
    assert statuses_page.has_visible_text(name, "td"), "Созданный статус не появился в списке"


def test_edit_status_updates_row(statuses_page, unique):
    new_name = f"Draft {unique}"
    statuses_page.rename(SEEDED_STATUS_NAME, new_name)
    statuses_page.open_list()
    assert statuses_page.has_visible_text(new_name, "td")


def test_delete_status_removes_row(statuses_page):
    statuses_page.delete(SEEDED_STATUS_NAME)
    statuses_page.open_list()
    assert statuses_page.wait_text_gone(SEEDED_STATUS_NAME, "td")
    assert len(statuses_page.visible_rows()) == SEEDED_STATUSES_COUNT - 1


def test_bulk_delete_empties_status_list(statuses_page):
    statuses_page.open_list()
    statuses_page.bulk_delete()
    assert statuses_page.has_visible_text("Do you want to add one?"), "Список не опустел"
