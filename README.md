# smena-assignment

### [Задание по ссылке](https://github.com/pakodev28/assignments/blob/master/backend/README.md)

## Как развернуть проект из файла docker-compose(используется gunicorn и postgresql):
1. Склонировать проект, настроить .env файл:
    ```
    git clone git@github.com:pakodev28/smena-assignment.git
    ```
    ```
    cd smena-assignment
    ```
    ```
    cp .env.example .env
    ```
2. для запуска контейнеров:
    ```
    docker-compose up -d --build
    ```
3. Далее выполните следующие команды:
    ```
    docker-compose exec web python manage.py migrate --noinput
    ```
    ```
    docker-compose exec web python manage.py collectstatic --noinput
    ```
    ```
    docker-compose exec web python manage.py createsuperuser
    ```

4. Можете загрузить Printers в БД:
    ```
    docker-compose exec web python manage.py loaddata fixtures.json
    ```

5. Запуск Django-RQ:
    ```
    docker-compose exec web python manage.py rqworker default
    ```
6. Остановите контейнеры:
    ```
    docker-compose down -v
    ```

### API

Описание доступных методов находится в файле api.yml (swagger-спецификация). Можно отрендерить через [онлайн редактор](https://editor.swagger.io/) или через соответствующий плагин для PyCharm или VSCode
