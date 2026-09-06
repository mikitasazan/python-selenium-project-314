"""Фикстуры, общие для тестовых модулей.

Данные приложения живут в памяти вкладки и восстанавливаются при каждой
перезагрузке страницы. Браузер поднимается заново на каждый тест, поэтому
списки всегда начинаются с одного и того же набора записей.
"""

from __future__ import annotations

import uuid

import pytest

from .pages.labels import LabelsPage
from .pages.login import LoginPage
from .pages.statuses import StatusesPage
from .pages.tasks import TasksPage
from .pages.users import UsersPage


@pytest.fixture
def signed_in(driver, base_url) -> LoginPage:
    page = LoginPage(driver, base_url)
    page.sign_in()
    assert page.dashboard_is_visible(), "После входа не появилось содержимое дашборда"
    return page


@pytest.fixture
def users_page(driver, base_url, signed_in) -> UsersPage:
    return UsersPage(driver, base_url)


@pytest.fixture
def statuses_page(driver, base_url, signed_in) -> StatusesPage:
    return StatusesPage(driver, base_url)


@pytest.fixture
def labels_page(driver, base_url, signed_in) -> LabelsPage:
    return LabelsPage(driver, base_url)


@pytest.fixture
def tasks_page(driver, base_url, signed_in) -> TasksPage:
    return TasksPage(driver, base_url)


@pytest.fixture
def unique() -> str:
    return uuid.uuid4().hex[:6]
