![example workflow](https://github.com/anton-sivko/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Проект доступен по адресу: http://84.201.130.177/, 
админ: anton, пароль: 555 
Пользователь: email: b@b.ru 
пароль: bender555

Foodgram - «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
При пуше в ветку master автоматически отрабатывают сценарии:
1. Автоматический запуск тестов,
2. Обновление образов на Docker Hub,
3. Автоматический деплой на боевой сервер.

### Технологии:

    Python 3.7.0
    Django 3.2.18
    DRF 3.12.4
    PostgreSQL
    Nginx
    gunicorn
    Docker

На удаленном сервере необходимо установить Docker и docker-compose:
```
curl -fsSL https://get.docker.com -o get-docker.sh
```
```
sh get-docker.sh
```
```
apt install docker-compose
```
Скопируйте файлы docker-compose.yaml и nginx.conf из вашего проекта 
на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx.conf соответственно.

```
scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/
```
В репозитории на GitHub необходимо прописать Secrets - переменные доступа к вашим сервисам и настроек БД.
Переменые прописаны в workflows/foodgram-project-react .yaml

* DOCKER_PASSWORD, DOCKER_USERNAME - для загрузки и скачивания образа с DockerHub 
* USER, HOST, PASSPHRASE, SSH_KEY - для подключения к удаленному серверу 

* DB_ENGINE - указываем, что работаем с postgres
* ALLOWED_HOSTS - разрешенные хосты, разделенные запятой.
* DEBUG - режим отладки, указать 0 или 1.
* DB_NAME - имя БД
* POSTGRES_USER - логин для подключения к базе данных
* POSTGRES_PASSWORD - пароль для подключения к БД
* DB_HOST - название сервиса (контейнера)
* DB_PORT - порт для подключения к БД

### Развертывание приложения

 При пуше в ветку master приложение пройдет тесты, обновит образ на DockerHub и сделает деплой на сервер.
 После этого Вам необходимо выполнить следующие действия:
1. Подключитесь к серверу
```
ssh <USER>@<HOST>
```
2. Перейдите в запущенный контейнер приложения командой:
```
docker container exec -it <CONTAINER ID> bash
```
3. Внутри контейнера необходимо выполнить миграции и собрать статику приложения:
```
docker-compose exec backend python manage.py migrate --noinput
```
```
docker-compose exec backend python manage.py collectstatic --no-input
```
4. Для использования панели администратора по адресу http://84.201.130.177/admin/ необходимо создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
5. Заполните, при необходимости, базу начальными данными:
```
docker-compose exec backend python manage.py loaddata fixtures.json
```

Документация API доступна по эндпойнту: 

http://84.201.130.177/redoc/

### Авторы:
Антон Сивко.


foodgram-project-react 
