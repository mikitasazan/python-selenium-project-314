"""Настройка окружения тестов.

Адрес приложения приходит одной переменной `APP_BASE_URL`. Всё остальное —
браузер, размер окна, таймауты, каталог логов — имеет разумные значения по
умолчанию и переопределяется переменными окружения.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

LOGGER_NAME = "kanban.tests"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"

CHROME_BINARIES = (
    os.getenv("CHROME_BIN", ""),
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
)

CHROMEDRIVER_BINARIES = (
    os.getenv("CHROMEDRIVER_BIN", ""),
    "/usr/bin/chromedriver",
    "/usr/local/bin/chromedriver",
)


@dataclass(frozen=True, slots=True)
class Settings:
    base_url: str
    headless: bool
    window_size: str
    page_load_timeout: int
    implicit_wait: float
    log_level: str
    log_dir: Path
    screenshots_dir: Path


def _first_existing(candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def _read_settings() -> Settings:
    base_url = os.getenv("APP_BASE_URL")
    if not base_url:
        message = (
            "Не задана переменная APP_BASE_URL. "
            "Укажите адрес запущенного приложения, например http://127.0.0.1:5173"
        )
        raise RuntimeError(message)

    log_dir = Path(os.getenv("TEST_LOG_DIR", "test-results")).resolve()
    screenshots_dir = log_dir / "screenshots" / (urlparse(base_url).hostname or "app")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    headless = os.getenv("HEADLESS", "true").strip().lower() not in {"false", "0", "no"}

    return Settings(
        base_url=base_url.rstrip("/"),
        headless=headless,
        window_size=os.getenv("BROWSER_WINDOW_SIZE", "1440,900"),
        page_load_timeout=int(os.getenv("PAGE_LOAD_TIMEOUT", "45")),
        implicit_wait=float(os.getenv("SELENIUM_IMPLICIT_WAIT", "0.2")),
        log_level=os.getenv("TEST_LOG_LEVEL", "INFO").upper(),
        log_dir=log_dir,
        screenshots_dir=screenshots_dir,
    )


def _build_options(settings: Settings) -> Options:
    options = Options()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--window-size={settings.window_size}")
    binary = _first_existing(CHROME_BINARIES)
    if binary:
        options.binary_location = binary
    return options


def _build_service() -> Service | None:
    """Отдать драйвер из системы, если он там есть.

    Selenium Manager ищет драйвер в сети и не наводится на chromium. В образе
    проверки драйвер уже установлен, поэтому путь передаётся явно.
    """
    driver_path = _first_existing(CHROMEDRIVER_BINARIES)
    return Service(executable_path=driver_path) if driver_path else None


def _safe_name(nodeid: str) -> str:
    return re.sub(r"[^\w.-]", "_", nodeid.replace("::", "__").replace("/", "_"))


@pytest.fixture(scope="session")
def settings() -> Settings:
    return _read_settings()


@pytest.fixture(scope="session")
def app_logger(settings: Settings) -> logging.Logger:
    logging.basicConfig(level=settings.log_level, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(settings.log_level)
    if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        settings.log_dir.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(settings.log_dir / "pytest.log", mode="a", encoding="utf-8")
        handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
        logger.addHandler(handler)
    return logger


@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    return settings.base_url


@pytest.fixture
def driver(settings: Settings, app_logger: logging.Logger, request: pytest.FixtureRequest):
    browser = webdriver.Chrome(options=_build_options(settings), service=_build_service())
    browser.set_page_load_timeout(settings.page_load_timeout)
    browser.implicitly_wait(settings.implicit_wait)
    browser.get(settings.base_url)
    browser.delete_all_cookies()
    try:
        browser.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    except WebDriverException as error:
        app_logger.warning("Не удалось очистить хранилище браузера: %s", error)

    try:
        yield browser
    finally:
        report = getattr(request.node, "rep_call", None)
        if report is not None and report.failed:
            path = settings.screenshots_dir / f"{_safe_name(request.node.nodeid)}.png"
            try:
                browser.save_screenshot(str(path))
                app_logger.info("Снимок экрана упавшего теста: %s", path)
            except WebDriverException as error:
                app_logger.error("Снимок экрана не сохранён: %s", error)
        browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
