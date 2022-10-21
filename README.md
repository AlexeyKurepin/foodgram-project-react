# Cервис 'Foodgram'

### Описание
Приложение в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов,
необходимых для приготовления выбранных блюд.

Проект доступен по адресу - <a href="http://178.154.241.81">178.154.241.81</a>

### Используемые технологии:

- __Python__
- __Django__
- __Django Rest Framework__
- __Gunicorn__
- __NGINX__
- __PostgreSQL__
- __Docker__

### Как развернуть проект локально:

Клонировать репозиторий:

```
git@github.com:AlexeyKurepin/foodgram-project-react.git
```
__Запустить проект в контейнерах Docker:__

перейти в каталог **`infra`** и создать файл **`.env`**:
```angular2html
cd infra
touch .env
```
запонить его данными:
```angular2html
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=1234567890
```

выполнить команду:
```
docker-compose up -d
```
провести миграции:
```
docker-compose exec backend python manage.py migrate
```
создать суперпользователя:
```
docker-compose exec bakend python manage.py createsuperuser
```
собрать статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
заполненить базу данными:
```angular2html
docker-compose exec backend python manage.py loaddata dump.json
```
__После запуска проект будут доступен по адресу: http://localhost/__

####Автор проекта:

<a href= "https://github.com/AlexeyKurepin">__Алексей Курепин__<a/>



![foodgram workflow status](https://github.com/AlexeyKurepin/foodgram-project-react/actions/workflows/main.yml/badge.svg)
![](https://camo.githubusercontent.com/05af48edd09a6c4eb649d00a8e38dbf22b6a8dc4b7125db48cd9e91b4c3ca1a6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e2d332e372e302d626c75653f7374796c653d666c6174266c6f676f3d707974686f6e266c6f676f436f6c6f723d7768697465)
![](https://camo.githubusercontent.com/1eda6ac88c4f1647ce3c949b141faf8bcf9b9fc68b065e69018b6e79490f15d3/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d332e322e31352d6f72616e67653f7374796c653d666c6174266c6f676f3d646a616e676f266c6f676f436f6c6f723d7768697465)
![](https://camo.githubusercontent.com/bc3878ac2fdac5012a23088d36d31df52f74d2b14663b22cfdd2fa5745f9805c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f506f737467726553514c2d31332e302d626c75653f7374796c653d666c6174266c6f676f3d706f737467726573716c266c6f676f436f6c6f723d7768697465)