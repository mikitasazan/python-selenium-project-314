"""Шаг 20: приложение поднимается и рисует интерфейс."""

from selenium.webdriver.common.by import By

from .pages.login import LoginPage


def test_smoke_application_renders(driver, base_url):
    """Открытая страница показывает форму входа, а не пустой экран."""
    page = LoginPage(driver, base_url)
    page.open_form()
    assert page.form_is_visible()


def test_smoke_page_has_title(driver, base_url):
    driver.get(base_url)
    assert driver.title.strip() != ""
    assert driver.find_element(By.ID, "root").is_displayed()
