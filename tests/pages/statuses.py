"""Раздел «Статусы» — колонки канбан-доски."""

from __future__ import annotations

from .base import BasePage


class StatusesPage(BasePage):
    route = "task_statuses"

    def open_list(self) -> None:
        self.open()
        self.visible_text("Slug", "span")

    def create(self, name: str, slug: str) -> None:
        self.open_list()
        self.click_button("Create")
        self.fill('input[name="name"]', name)
        self.fill('input[name="slug"]', slug)
        self.save()

    def open_row(self, text: str) -> None:
        self.open_list()
        self.click_text(text, "td")

    def rename(self, current_name: str, new_name: str) -> None:
        self.open_row(current_name)
        self.fill('input[name="name"]', new_name)
        self.save()

    def delete(self, name: str) -> None:
        self.open_row(name)
        self.click_button("Delete")
