## Запуск проекта

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Запуск тестов

```bash
python manage.py test -v2
```