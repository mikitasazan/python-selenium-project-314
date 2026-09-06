"""Форма входа и выход из приложения."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from ..constants import CREDENTIALS, DASHBOARD_TEXT
from .base import BasePage

USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="username"]')
PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[name="password"]')
SUBMIT_BUTTON = (By.XPATH, '//button[normalize-space()="Sign in"]')
PROFILE_BUTTON = (By.CSS_SELECTOR, '[aria-label="Profile"]')


class LoginPage(BasePage):
    route = "login"

    def open_form(self) -> None:
        self.open()
        self.visible(USERNAME_INPUT)

    def form_is_visible(self) -> bool:
        return all(
            element.is_displayed()
            for element in (
                self.visible(USERNAME_INPUT),
                self.visible(PASSWORD_INPUT),
                self.visible(SUBMIT_BUTTON),
            )
        )

    def sign_in(self, username: str | None = None, password: str | None = None) -> None:
        self.open_form()
        self.fill('input[name="username"]', username or CREDENTIALS["username"])
        self.fill('input[name="password"]', password or CREDENTIALS["password"])
        self.clickable(SUBMIT_BUTTON).click()

    def dashboard_is_visible(self) -> bool:
        """Вход считается успешным, только если видно содержимое дашборда.

        Кнопка профиля в шапке появляется и тогда, когда за формой пусто,
        поэтому одной её мало.
        """
        return self.text_stays_visible(DASHBOARD_TEXT)

    def sign_out(self) -> None:
        self.clickable(PROFILE_BUTTON).click()
        self.clickable((By.XPATH, '//li[@role="menuitem" and normalize-space()="Logout"]')).click()
