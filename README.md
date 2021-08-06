## Описание.
Обучающий сайт "Food Academy".

Layout:
```
app/ - проект
    manage.py
    api/ - REST API + JWT Authentication
       tests/
       apps.py
       paginators.py
       serializers.py
       urls.py
       views.py
    config/
        settings/
            base.py - общие настройки
            dev.py  - настройки development
            prod.py - настройки production
        urls.py - настройки URL
        wsgi.py - настройки WSGI
    contactus/  - приложение для обратной связи
        migrations/ 
        tests/    
        admin.py
        apps.py
        models.py
        urls.py
    courses/    - основное приложение (курсы, группы, расписание)
        management/
            commands/
                add_courses.py
        migrations/ 
        tests/     
        admin.py
        app.py
        models.py
        urls.py
    users/  - приложение для управления пользоваталями (администраторы, преподаватели, студенты)
        management/
            commands/   
                add_users.py
                create_administrator.py
        migrations/ 
        tests/     
        admin.py
        app.py
        managers.py
        models.py
        urls.py
deploy/ - вспомогательные файлы для развёртывания проекта.
```
Для авторизации используется custom-модель (авторизация по уникальному e-mail).

### Установка и запуск (пример для Linux).
```
# mkdir FoodAcademy
# cd FoodAcademy/
# git clone https://github.com/nikitasellin/FoodAcademy2.git .
```
**Важно! В целях безопасности, рекомендуется сменить секретный ключ, реквизиты доступа к БД и пару e-mail/пароль администратора в
файлах .env и config/dev.py**

Запуск.
```
# docker-compose build
# docker-compose up [-d]
```
После успешного запуска, интерфейс доступен по адресу:
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/ (Администрирование Django)
```
Примечание: при первом запуске производится автоматическое заполнение БД фейковыми данными (преподаватели, курсы) и создание администратора.
При необходимости (после очистки БД), можно произвести эти действия вручную:
```
# docker-compose exec app ./manage.py add_users
# docker-compose exec app ./manage.py add_courses
# docker-compose exec app ./manage.py manage.py create_administrator --email $ADMIN_USER --password $ADMIN_PASSWORD --first_name Super --last_name User
```
Администратору доступно добавление/редактирование курсов и преподавателей в интерфейсе.

### API.
Реализован на DRF + JWT Authentication для моделей Course, Teacher и Message.

Доступ без авторизации:

    /api/ - API root 
    /api/view/ - список ссылок, доступных без авторизации
    /api/view/courses/ - просмотр списка курсов
    /api/view/courses/<int:id>/ - просмотр информации об одном курсе
    /api/view/teachers/ - просмотр списка предователей
    /api/view/teachers/<int:id>/ - просмотр информации об одном преподавателе

Доступ только для администратора:

    /api/full-access/ - список ссылок, доступных администратору
    /api/full-access/courses/ - просмотр списка курсов, добавление курса
    /api/full-access/courses/<int:id>/ - просмотр/редактирование/удаление курса
    /api/full-access/teachers/ - просмотр списка курсов, добавление преподавателя
    /api/full-access/teachers/<int:id>/ - просмотр/редактирование/удаление преподавателя
    /api/full-access/messages/ - просмотр списка сообщений, отправленных через форму на сайте
    /api/full-access/messages/<int:id>/ - просмотр/редактирование/удаление одного сообщения (для редактирования доступен только статус)

Доступ для авторизованного студента:
 
    /api/full-access/groups/<int:id>/ - запись на курс

Авторизация:

    /api/token/obtain/ - сгенерировать пару токенов
    /api/token/refresh/ - обновить access токен

Генерация/обновление токена доступны в личном кабинете:
    
    для генерации токена необходимо заполнить поле "пароль"
    для обновления токена необходимо заполнить поле "Refresh token" (после успешной генерации пары токенов заполняется автоматически)

### GraphQL.

Интерфейс GraphQL доступен по адресу:
```
http://127.0.0.1:8000/graphql/
```
Пример запроса для получения списка всех курсов с преподавателями и группами:
```
{
  allCourses {
    id
    title
    courseGroup {
      id
      title
      students {
        id
        fullName
      }
    }
    teachers {
      id
      fullName
    }    
  }
}
```

### Тестирование.

Запуск тестов для backend:
```
# docker-compose exec app python manage.py test
```

### Frontend.

Интерфейс на React доступен по адресу:
```
http://127.0.0.1:3000 (dev server)
```
