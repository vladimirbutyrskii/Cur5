Описание проекта.

В рамках проекта необходимо получить данные о компаниях и вакансиях с сайта hh.ru, 
спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

Основные этапы проекта.

1. Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого использовать публичный API hh.ru и библиотеку requests .
2. Выбрать не менее 10 интересных компаний, от которых получаем данные о вакансиях по API.
3. Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используется библиотека psycopg2.
4. Реализовать код, заполняющий созданные в БД таблицы данными о работодателях и их вакансиях.
5. Создать класс DBManager для работы с данными в БД.

Класс DBManager.

Класс DBManager должен будет подключаться к БД и иметь следующие методы:

get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.

get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

get_avg_salary() — получает среднюю зарплату по вакансиям.

get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python. Класс DBManager должен использовать библиотеку psycopg2 для работы с БД.

Решение должно быть выложено на GitHub. 

Оформить файл README.md с информацией о назначении проекта и деталях его работы. 

Описание. 

В рамках проекта создана БД на основе данных, полученных по API.
БД состоит из двух таблиц:

employers

vacancies

В ходе работы при заполнении БД используется временная таблица.

Конфигурация БД используется из database.ini.



Работа пользователя проходит через меню, где реализованы основные потребности заказчика.
1. Вывод на экран списка всех компаний и количество вакансий в каждой из них.
2. Вывод на экран списка всех вакансий с указанием названий компании, вакансии, уровня зарплаты (н/у - не указана), ссылки на вакансию.
3. Вывод на экран средней зарплаты по вакансиям (только для российских рублей).
4. Вывод на экран списка вакансий, зарплата которых выше среднего уровня заработной платы по вакансиям.
5. Вывод на экран списка названий вакансий, где присутствуют введенные ключевые слова (одно или несколько).
6. Обновление БД вакансий с сайта HH.RU
7. Выход.
