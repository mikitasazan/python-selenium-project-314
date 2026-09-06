"""Шаг 30: вход и выход."""

from .pages.login import LoginPage


def test_sign_in_shows_dashboard(driver, base_url):
    page = LoginPage(driver, base_url)
    page.sign_in()
    assert page.dashboard_is_visible(), "За формой входа не оказалось содержимого"


def test_sign_in_shows_navigation_menu(driver, base_url):
    page = LoginPage(driver, base_url)
    page.sign_in()
    assert page.dashboard_is_visible()
    for section in ("Tasks", "Users", "Labels", "Task statuses"):
        assert page.has_visible_text(section), f"В меню нет раздела {section}"


def test_sign_out_returns_login_form(driver, base_url):
    page = LoginPage(driver, base_url)
    page.sign_in()
    assert page.dashboard_is_visible()
    page.sign_out()
    assert page.form_is_visible(), "После выхода форма входа не показана"
