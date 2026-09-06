"""Общий предок страниц.

Правило одно: любое ожидание здесь — про ВИДИМОСТЬ или кликабельность, а не
про присутствие узла в DOM. Тест, довольный самим фактом наличия элемента,
не замечает сломанного раздела и потому ничего не проверяет.
"""

from __future__ import annotations

import logging
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..constants import DEFAULT_TIMEOUT, LOGGER_NAME
from ..utils.xpath import by_text

logger = logging.getLogger(LOGGER_NAME)

SETTLE_INTERVAL = 0.3

SELECT_ALL_BOX = (By.CSS_SELECTOR, "table thead th .MuiCheckbox-root")
SELECT_ALL_INPUT = (By.CSS_SELECTOR, 'table thead th input[type="checkbox"]')


class BasePage:
    route = ""

    def __init__(self, driver, base_url: str) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # --- навигация -------------------------------------------------------

    def open(self, route: str | None = None) -> None:
        fragment = self.route if route is None else route
        fragment = fragment.lstrip("/")
        url = f"{self.base_url}/#/{fragment}" if fragment else self.base_url
        self.driver.get(url)

    # --- ожидания --------------------------------------------------------

    def visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def present(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible_text(self, text: str, tag: str = "*") -> WebElement:
        return self.visible((By.XPATH, by_text(text, tag)))

    def has_visible_text(self, text: str, tag: str = "*") -> bool:
        try:
            self.visible_text(text, tag)
        except TimeoutException:
            return False
        return True

    def text_is_shown_now(self, text: str, tag: str = "*") -> bool:
        """Виден ли текст прямо сейчас, без ожидания."""
        found = self.driver.find_elements(By.XPATH, by_text(text, tag))
        return any(element.is_displayed() for element in found)

    def text_stays_visible(self, text: str, tag: str = "*", samples: int = 4) -> bool:
        """Текст появился и не исчез.

        Раздел, который отрисовался и тут же спрятался, для пользователя
        сломан. Одной мгновенной проверки на видимость мало: она успевает
        поймать кадр до того, как содержимое пропало.
        """
        if not self.has_visible_text(text, tag):
            return False
        for _ in range(samples):
            time.sleep(SETTLE_INTERVAL)
            if not self.text_is_shown_now(text, tag):
                return False
        return True

    def element_stays_visible(self, locator: tuple[str, str], samples: int = 4) -> bool:
        """Элемент появился и остался виден.

        То же, что `text_stays_visible`, но по локатору: нужно там, где
        проверяется значение поля, а не текст на странице.
        """
        try:
            element = self.visible(locator)
        except TimeoutException:
            return False
        for _ in range(samples):
            time.sleep(SETTLE_INTERVAL)
            if not element.is_displayed():
                return False
        return True

    def wait_text_gone(self, text: str, tag: str = "*") -> bool:
        locator = (By.XPATH, by_text(text, tag))
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False
        return True

    # --- действия --------------------------------------------------------

    def click_text(self, text: str, tag: str = "*") -> WebElement:
        element = self.clickable((By.XPATH, by_text(text, tag)))
        element.click()
        return element

    def click_button(self, aria_label: str) -> WebElement:
        element = self.clickable((By.CSS_SELECTOR, f'[aria-label="{aria_label}"]'))
        element.click()
        return element

    def fill(self, css: str, value: str) -> WebElement:
        field = self.clickable((By.CSS_SELECTOR, css))
        field.click()
        field.send_keys(Keys.CONTROL + "a", Keys.COMMAND + "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(value)
        return field

    def choose(self, css: str, option: str) -> None:
        """Выбрать значение в выпадающем списке MUI.

        В разметке `input[name=...]` скрыт, кликать надо по соседнему
        `role="combobox"`.
        """
        field = self.present((By.CSS_SELECTOR, css))
        trigger = field
        if field.tag_name.lower() == "input":
            found = self.driver.find_elements(
                By.XPATH,
                f'//input[@name="{field.get_attribute("name")}"]'
                '/ancestor::div[contains(@class,"MuiFormControl-root")][1]'
                '//*[@role="combobox"]',
            )
            if found:
                trigger = found[0]
        self.wait.until(lambda _: trigger.is_displayed() and trigger.is_enabled())
        trigger.click()
        self.clickable((By.XPATH, by_text(option, "li"))).click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".MuiBackdrop-root")))

    def save(self) -> None:
        self.click_button("Save")

    # --- таблицы ---------------------------------------------------------

    def visible_rows(self) -> list[WebElement]:
        self.visible((By.CSS_SELECTOR, "table tbody tr"))
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        return [row for row in rows if row.is_displayed()]

    def select_all_rows(self) -> None:
        """Отметить все строки.

        Сам `input` у чекбокса MUI прозрачен, и Selenium считает его
        невидимым. Кликаем по видимой обёртке, а состояние читаем по input-у:
        `is_selected` работает и для скрытого элемента.
        """
        self.clickable(SELECT_ALL_BOX).click()
        checkbox = self.present(SELECT_ALL_INPUT)
        self.wait.until(lambda _: checkbox.is_selected())

    def bulk_delete(self) -> None:
        self.select_all_rows()
        self.click_button("Delete")
