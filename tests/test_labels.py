"""Шаг 60: раздел «Метки»."""

from .constants import SEEDED_LABEL_NAME, SEEDED_LABELS_COUNT


def test_label_list_shows_records(labels_page):
    labels_page.open_list()
    assert labels_page.has_visible_text("Name", "span")
    assert labels_page.text_stays_visible(SEEDED_LABEL_NAME, "td"), "Строки списка не держатся"
    assert len(labels_page.visible_rows()) == SEEDED_LABELS_COUNT


def test_create_label_adds_row(labels_page, unique):
    name = f"regression-{unique}"
    labels_page.create(name)
    labels_page.open_list()
    assert labels_page.has_visible_text(name, "td"), "Созданная метка не появилась в списке"


def test_edit_label_updates_row(labels_page, unique):
    new_name = f"defect-{unique}"
    labels_page.rename(SEEDED_LABEL_NAME, new_name)
    labels_page.open_list()
    assert labels_page.has_visible_text(new_name, "td")


def test_delete_label_removes_row(labels_page):
    labels_page.delete(SEEDED_LABEL_NAME)
    labels_page.open_list()
    assert labels_page.wait_text_gone(SEEDED_LABEL_NAME, "td")
    assert len(labels_page.visible_rows()) == SEEDED_LABELS_COUNT - 1


def test_bulk_delete_empties_label_list(labels_page):
    labels_page.open_list()
    labels_page.bulk_delete()
    assert labels_page.has_visible_text("Do you want to add one?"), "Список не опустел"
