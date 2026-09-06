"""Раздел «Пользователи»."""

from __future__ import annotations

from .base import BasePage


class UsersPage(BasePage):
    route = "users"

    def open_list(self) -> None:
        self.open()
        self.visible_text("Email", "span")

    def create(self, email: str, first_name: str, last_name: str) -> None:
        self.open_list()
        self.click_button("Create")
        self.fill('input[name="email"]', email)
        self.fill('input[name="firstName"]', first_name)
        self.fill('input[name="lastName"]', last_name)
        self.save()

    def open_row(self, text: str) -> None:
        self.open_list()
        self.click_text(text, "td")

    def edit_first_name(self, email: str, new_first_name: str) -> None:
        self.open_row(email)
        self.fill('input[name="firstName"]', new_first_name)
        self.save()

    def delete(self, email: str) -> None:
        self.open_row(email)
        self.click_button("Delete")

    def submit_email(self, email: str) -> None:
        """Отправить форму создания с заведомо неверным адресом."""
        self.open_list()
        self.click_button("Create")
        self.fill('input[name="email"]', email)
        self.fill('input[name="firstName"]', "Anna")
        self.fill('input[name="lastName"]', "Tester")
        self.save()
