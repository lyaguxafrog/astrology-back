#!flask/bin/python

# Импорт необходимых библиотек и модулей
import sys
from app import app

if __name__ == '__main__':
    # Проверка, запущен ли скрипт с аргументом 'tests' (для запуска тестов)
    if len(sys.argv) > 1 and sys.argv[1] == 'tests':
        import unittest
        # Поиск и запуск всех тестов из директории 'tests'
        tests = unittest.TestLoader().discover('tests')
        # Запуск тестов и вывод результатов в консоль
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        # Если все тесты успешно прошли, завершиться с кодом 0
        if result.wasSuccessful():
            sys.exit(0)
        # Если есть неуспешные тесты, завершиться с кодом 1
        else:
            sys.exit(1)
    else:
        # Если скрипт запущен без аргумента 'tests', запустить Flask-приложение в режиме отладки
        if __name__ == '__main__':
            app.run(debug=True)
