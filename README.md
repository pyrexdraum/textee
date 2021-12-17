# Textee
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/pyrexdraum/textee?logo=Python)
[![Django](https://img.shields.io/badge/Django-3.2-success?style=flat&logo=Django)](https://docs.djangoproject.com/en/3.2/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.1-success?style=flat&logo=PostgreSQL)](https://www.postgresql.org/docs/14/index.html)
[![NGINX](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX)](https://nginx.org/)
[![Gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=Gunicorn)](https://gunicorn.org/)
[![RabbitMQ](https://img.shields.io/badge/-RabbitMQ-464646?style=flat&logo=RabbitMQ)](https://www.rabbitmq.com/)
[![Celery](https://img.shields.io/badge/-Celery-464646?style=flat&logo=Celery)](https://docs.celeryproject.org/en/stable/)

Textee - это веб-сайт, на котором вы можете хранить любой текст
онлайн для удобства обмена. Веб-сайт в основном используется 
программистами для хранения фрагментов исходного кода или 
информации о конфигурации, но любой желающий может вставить 
любой текст, выбрать срок действия и синтаксис.

## Стек технологий
### Back-end

- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [Celery](https://github.com/celery/celery)
- [NGINX](https://nginx.org/ru/)
- [Docker](https://www.docker.com/)

### Front-end

- [Bootstrap](https://getbootstrap.com/)

## Техническое описание
**Сниппет** - фрагмент текста или кода программы, содержит:
 - **Автора**, если создан зарегистрированным пользователем.
 - **Заголовок**, не более 100 символов.
 - **Текст**, не более 65 536 символов (256 KiB).
 - **Синтаксис**, для выделения синтаксических конструкций текста 
с использованием различных цветов, шрифтов и начертаний.
 - **Время и дату создания**.
 - **Срок действия**, время, через которое сниппет будет удалён.
 - **URL**, ссылка, по которой можно получить сниппет.
 
### Главная страница
Отображает форму для создания сниппета. 
Сниппет может создать любой пользователь. 
Если пользователь вошёл в систему, созданный сниппет автоматически закрепляется за ним.

### Страница просмотра сниппета
После создания сниппета, пользователь будет перенаправлен на эту страницу.
На этой странице отображается созданный сниппет. 
Если у сниппета указан синтаксис, то на странице отображается форматированный 
текст в соответствии с синтаксисом в дополнение к исходному тексту.
Для пользователя вошедшего в систему, отображаются кнопки редактирования и удаления сниппета.

### Страница профиля пользователя
Данная страница содержит все сниппеты, который создал пользователь.
Эту страницу может посетить любой пользователь.

### Страницы связанные с аутентификацией:
  - Страница входа в систему
  - Страница выхода из системы
  - Страница регистрации нового пользователя
  - Страница подтверждения почты
  - Страница настройки почты
  - Страница смены пароля
  - Страница сброса пароля

Сайт управляется системой Django Admin Site (необходима учетная запись супер-пользователя).

## Запуск проекта через docker-compose
Для запуска проекта вам потребуется установленный [Docker Engine](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/#install-compose) на вашей ОС.

### 1. Склонируйте репозиторий
```
git clone https://github.com/pyrexdraum/textee.git
```
Если у вас нет `git` скачайте [архив с проектом](https://github.com/pyrexdraum/textee/archive/refs/heads/main.zip) и распакуйте его.

### 2. Создайте `.env` файл
В папке `src` создайте файл `.env` и заполните его следующим содержимым:
```
DJANGO_SECRET_KEY=ваш_секретный_ключ_больше_50_символов

# перечислите через запятую ваш <публичный_ip>, <домен_сайта>, <www.домен_сайта>
DJANGO_ALLOWED_HOSTS=localhost, 127.0.0.1

POSTGRES_PASSWORD=пароль_от_базы_данных
```
замените собственными значениями.

### 3. Отредактируйте `nginx/textee.conf` файл
В папке `nginx` откройте файл `textee.conf` и добавьте после `localhost` ваш <публичный_ip>, <домен_сайта>, <www.домен_сайта>.
Пример:
```
upstream app {
    server django:8000;
}
server {
    listen 80;
    server_name localhost 8.8.8.8 your.site www.your.site;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /home/app/web/staticfiles/;
    }
}
```

### 4. Запустите проект
Внутри папки с проектом запустите команду (может потребоваться sudo для Linux)
```
docker-compose up -d --build
```
Потребуется некоторое время для запуска проекта.

### 5. Создайте супер-пользователя
После того как проект запущен, выполните:
```
docker exec -it textee_django_1 bash -c "python manage.py createsuperuser"
```
Заполните данные.

---

После этого можете зайти на сайт администрирования `/admin/` и управлять сайтом.


*Примечание*: по умолчанию регистрация не требует подтверждения почты, но вы можете настроить это поведение в файле `src/config/settings.py`, в комментариях присутствуют ссылки по настройке.


## От автора
Это мой первый проект в котором я реализовал все полученные знания из книг и документаций по разработке.
В процессе разработки я столкнулся со многими проблемами, но благодаря внимательному чтению и понимаю документации я легко их решил.
Проект задумывался как [MVP](https://ru.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE_%D0%B6%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1%D0%BD%D1%8B%D0%B9_%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82). Идеей проекта послужил сайт [pastebin](https://pastebin.com/).

Спасибо за внимание. 
