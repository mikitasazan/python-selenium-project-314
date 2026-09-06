# Тестирование канбан-доски с Selenium (Python)

[![hexlet-check](https://github.com/mikitasazan/python-selenium-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/mikitasazan/python-selenium-project-314/actions)

UI-тесты менеджера задач на Selenium WebDriver и pytest. Приложение — SPA на
react-admin без бэкенда: данные живут в памяти вкладки, поэтому каждый тест
получает свой браузер и одинаковый набор записей на старте.

Учебный проект Хекслета: https://ru.hexlet.io/programs/python-selenium

## Стек

- Python 3.14, pytest, Selenium 4
- Chrome или Chromium с драйвером
- uv для зависимостей

## Установка

```bash
git clone https://github.com/mikitasazan/python-selenium-project-314.git
cd python-selenium-project-314
make install
```

## Запуск

Поднять приложение:

```bash
make start
```

Прогнать тесты по нему:

```bash
make test
```

Посмотреть, что делает браузер: `HEADLESS=false make test`.

### Переменные окружения

| Переменная | Зачем | По умолчанию |
|---|---|---|
| `APP_BASE_URL` | адрес приложения, обязательна | — |
| `HEADLESS` | `false` показывает окно браузера | `true` |
| `BROWSER_WINDOW_SIZE` | размер окна | `1440,900` |
| `SELENIUM_DEFAULT_TIMEOUT` | предел явного ожидания, с | `10` |
| `PAGE_LOAD_TIMEOUT` | предел загрузки страницы, с | `45` |
| `CHROME_BIN` | путь к браузеру | ищется сам |
| `CHROMEDRIVER_BIN` | путь к драйверу | ищется сам |
| `TEST_LOG_DIR` | куда писать лог и снимки упавших тестов | `test-results` |

## Что проверяют тесты

| Файл | Сценарии |
|---|---|
| `tests/test_basic.py` | приложение открывается и рисует форму входа |
| `tests/test_auth.py` | вход открывает дашборд и меню, выход возвращает форму |
| `tests/test_users.py` | список, создание, правка, проверка адреса, удаление, групповое удаление |
| `tests/test_statuses.py` | список, создание, правка, удаление, групповое удаление |
| `tests/test_labels.py` | список, создание, правка, удаление, групповое удаление |
| `tests/test_tasks.py` | колонки и карточки доски, создание, правка, перенос между статусами, фильтр, карточка задачи |

Каждая проверка смотрит на видимый результат действия, а не на факт клика:
скрытый раздел приложения такой тест замечает, а проверка присутствия узла в
DOM — нет.

Взаимодействие со страницами вынесено в Page Object-классы `tests/pages/`,
подготовка входа и данных — в фикстуры `tests/conftest.py`. Ожидания —
только явные, `time.sleep` в коде нет.

## Структура

```
conftest.py          настройка браузера и адреса приложения
tests/constants.py   учётные данные, таймауты, стартовые записи
tests/pages/         Page Object на каждый раздел
tests/utils/         сборка XPath по видимому тексту
tests/test_*.py      сценарии по шагам проекта
```

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
