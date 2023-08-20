# Астрологическое приложение

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Астрологическое приложение - это веб-приложение, созданное с использованием Flask, которое позволяет пользователям вычислять астрологические данные, такие как градусы планет и домов, на основе введенных даты, времени и местоположения.

## Установка и запуск

Для установки и запуска приложения вам потребуется [Python](https://www.python.org/) версии 3.6+ и инструмент [Poetry](https://python-poetry.org/).

1. Склонируйте репозиторий на свой локальный компьютер.
2. Перейдите в корневую папку проекта.
3. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   ```
4. Активируйте виртуальное окружение Poetry:
   ```bash
   poetry shell
   ```
5. Запустите приложение:
   ```bash
   flask run
   ```
6. Перейдите в браузере по адресу `http://127.0.0.1:5000/`.

## Структура проекта

```
astrology-back/
│
├── app/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── planet_calculator.py
│   │   ├── house_calculators/
│   │   │   ├── __init__.py
│   │   │   ├── placidus.py
│   │   │   ├── koch.py
│   │   │   ├── equal.py
│   │   │   ├── porphyry.py
│   │   │   ├── regiomontanus.py
│   │   │   ├── campanus.py
│   │   │   ├── whole_sign.py
│   ├── templates/
│   │   ├── input.html
│   │   ├── result.html
│   ├── __init__.py
│   ├── author.py
│   ├── routes.py
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│
├── manage.py
├── pyproject.toml
├── poetry.lock
├── README.md
├── LICENSE
```

## Тестирование

Для запуска юнит-тестов, перейдите в папку проекта и выполните команду:
```bash
poetry run python manage.py tests
```

## Лицензия

Это приложение распространяется под лицензией MIT. Подробнее о лицензии можно узнать в файле [LICENSE](LICENSE).



## Автор

Адриан Макриденко [@lyaguxafrog](https://github.com/lyaguxafrog)

