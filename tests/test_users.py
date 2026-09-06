"""Шаг 40: раздел «Пользователи»."""

from selenium.webdriver.common.by import By

from .constants import SEEDED_USER_EMAIL, SEEDED_USERS_COUNT


def test_user_list_shows_records(users_page):
    """На списке видны и заголовки, и сами строки, а не только каркас."""
    users_page.open_list()
    for header in ("Email", "First name", "Last name"):
        assert users_page.has_visible_text(header, "span"), f"Нет колонки {header}"
    assert users_page.text_stays_visible(SEEDED_USER_EMAIL, "td"), "Строки списка не держатся"
    assert len(users_page.visible_rows()) == SEEDED_USERS_COUNT


def test_create_user_adds_row(users_page, unique):
    email = f"qa-{unique}@example.com"
    users_page.create(email, "Nina", "Petrova")
    users_page.open_list()
    assert users_page.has_visible_text(email, "td"), "Созданный пользователь не появился в списке"


def test_edit_form_prefills_record(users_page):
    users_page.open_row(SEEDED_USER_EMAIL)
    field = users_page.visible((By.CSS_SELECTOR, 'input[name="email"]'))
    assert field.get_attribute("value") == SEEDED_USER_EMAIL


def test_edit_user_updates_row(users_page, unique):
    new_name = f"Renamed{unique}"
    users_page.edit_first_name(SEEDED_USER_EMAIL, new_name)
    users_page.open_list()
    assert users_page.has_visible_text(new_name, "td"), "Новое имя не видно в списке"


def test_invalid_email_is_rejected(users_page):
    users_page.submit_email("not-an-email")
    assert users_page.has_visible_text("Incorrect email format")


def test_delete_user_removes_row(users_page):
    users_page.delete(SEEDED_USER_EMAIL)
    users_page.open_list()
    assert users_page.wait_text_gone(SEEDED_USER_EMAIL, "td")
    assert len(users_page.visible_rows()) == SEEDED_USERS_COUNT - 1


def test_bulk_delete_empties_user_list(users_page):
    users_page.open_list()
    users_page.bulk_delete()
    assert users_page.has_visible_text("Do you want to add one?"), "Список не опустел"
