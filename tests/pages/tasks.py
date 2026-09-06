"""Канбан-доска: карточки задач и колонки статусов."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from ..utils.xpath import by_text
from .base import BasePage

CARD = "div[contains(@class,'MuiCard-root')]"
COLUMN = "div[@data-rfd-droppable-id]"


class TasksPage(BasePage):
    route = "tasks"

    def open_board(self) -> None:
        self.open()
        self.clickable((By.CSS_SELECTOR, '[aria-label="Create"]'))

    # --- чтение доски ----------------------------------------------------

    def visible_cards(self) -> list[WebElement]:
        self.visible((By.XPATH, f"//{CARD}"))
        cards = self.driver.find_elements(By.XPATH, f"//{CARD}")
        return [card for card in cards if card.is_displayed()]

    def visible_column_titles(self) -> list[str]:
        titles = self.driver.find_elements(By.XPATH, f"//{COLUMN}/preceding-sibling::*[1]")
        return [title.text.strip() for title in titles if title.is_displayed()]

    def card_is_visible(self, title: str) -> bool:
        return self.has_visible_text(title, "div")

    def card_is_in_column(self, title: str, status_name: str) -> bool:
        column_xpath = f"{by_text(status_name)}/following::{COLUMN}[1]"
        card_xpath = f"{column_xpath}//{CARD}//*[normalize-space()='{title}']"
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, card_xpath)))
        except TimeoutException:
            return False
        return True

    # --- действия --------------------------------------------------------

    def create(self, title: str, content: str, assignee: str, status: str) -> None:
        self.open_board()
        self.click_button("Create")
        self.choose('input[name="assignee_id"]', assignee)
        self.fill('input[name="title"]', title)
        self.fill('textarea[name="content"]', content)
        self.choose('input[name="status_id"]', status)
        self.save()

    def _card_action(self, title: str, action: str) -> None:
        card_xpath = f"{by_text(title)}/ancestor::{CARD}"
        self.wait.until(EC.visibility_of_element_located((By.XPATH, card_xpath)))
        button_xpath = f"{card_xpath}//*[@aria-label='{action}']"
        self.clickable((By.XPATH, button_xpath)).click()

    def edit(
        self,
        title: str,
        *,
        new_title: str | None = None,
        new_status: str | None = None,
    ) -> None:
        self.open_board()
        self._card_action(title, "Edit")
        if new_title is not None:
            self.fill('input[name="title"]', new_title)
        if new_status is not None:
            self.choose('input[name="status_id"]', new_status)
        self.save()

    def open_details(self, title: str) -> None:
        self.open_board()
        self._card_action(title, "Show")

    def filter_by_status(self, status_name: str) -> None:
        self.open_board()
        self.choose('input[name="status_id"]', status_name)
