# Лабораторная работа № 2: Работа с SQLAlchemy и Alembic

## Запуск приложения

Для запуска приложения необходимо выполнить следующие шаги:

1. Убедиться, что у вас установлен Python 3.10

2. Создать и активировать виртуальное окружение:
   - В Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - В Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустить приложение:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```

После запуска приложение будет доступно по адресу: http://localhost:8001

## Альтернативный способ запуска

Также можно запустить приложение напрямую из файла main.py:
```bash
python -m app.main
