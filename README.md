<h1 align="center">Трекер расходов</h1>
<p align="center">
<a href="https://www.djangoproject.com/">
<img src="https://img.shields.io/badge/django-%23092E20.svg?style=flat&logo=django&logoColor=white"/>
</a>
<a href="https://www.django-rest-framework.org/">
<img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=flat&logo=django&logoColor=white&color=ff1709&labelColor=gray"/>
</a>
<a href="https://www.postgresql.org/">
<img src="https://img.shields.io/badge/postgres-%23316192.svg?style=flat&logo=postgresql&logoColor=white"/>
</a>
<a href="https://django-bootstrap-v5.readthedocs.io/en/latest/#">
<img src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=flat&logo=bootstrap&logoColor=white"/>
</a>
<img src="https://img.shields.io/github/commit-activity/m/Kozorez-V/expense-tracker?style=flat&color=purple"/>
<img src="https://img.shields.io/github/repo-size/Kozorez-V/expense-tracker?color=red"/>
</p>


Веб-приложение для отслеживания расходов.

## Задачи

- Учет расходов
- Ведение статистики расходов

## Функции

- Добавление, редактирование и удаление расходов
- Добавление, переименование и удаление категорий расходов
- Возможность устанавливать лимит расходов
- Статистика
- Регистрация/авторизация

## Категории по-умолчанию

- Дом
- Продукты
- Транспорт
- Здоровье
- Еда вне дома
- Развлечения
- Красота
- Образование
- Домашние животные

Всем пользователям при регистрации присваивается дефолтный набор категорий.

## Лимит

Периоды, на которые можно установить значение лимита:

- День
- Неделя
- Месяц

Чтобы убрать лимит, необходимо поставить 0 в качестве его значения.

## Технологии

- Python 3.10.2
- Django 4.0.5
- Django Rest Framework 3.13.1
- PostgreSQL 14.4
- Bootstrap 5


## Развертывание

Установите poetry, docker, docker-compose.

Для **Windows**

- `docker-compose up -d`
- `poetry run python expense_tracker/manage.py createsuperuser`
- Через адресную строку перейти по адресу
```
192.168.99.100:8080
```

Для **Linux**

- `sudo docker-compose up -d`
- `poetry run python expense_tracker/manage.py createsuperuser`
- `poetry run python expense_tracker/manage.py runserver`