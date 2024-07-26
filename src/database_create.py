import psycopg2

"""from utils import get_id_employees
from utils import get_vacancies
from settings import COMPANY_NAMES, EMPLOYEE_API, VACANCIES_API"""


def create_db(database_name: str, params: dict) -> None:
    """
    создание БД, таблиц и загрузка данных в таблицы
    :param vacancy:
    :return:
    """

    # Создание БД

    conn = psycopg2.connect(dbname="postgres", user="postgres", password="12345", host="127.0.0.1")
    cursor = conn.cursor()

    conn.autocommit = True
    # команда для создания базы данных
    sql = f"CREATE DATABASE {database_name}"
    cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")

    # выполняем код sql
    cursor.execute(sql)
    print("База данных успешно создана...")

    cursor.close()
    conn.commit()
    conn.close()

    # with psycopg2.connect(database_name, **params) as connection:  # with psycopg2.connect(**params) as connection:
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    # cur = conn.cursor()

    with conn.cursor() as cursor:
        #  Удаляем старые таблицы, если ранее существовали.
        cursor.execute(f"""
        DROP TABLE IF EXISTS vacancies CASCADE;
        DROP TABLE IF EXISTS employers CASCADE;
        """)

        # Создаем таблицы.
        cursor.execute(f"""

            CREATE TABLE vacancies (
            vacancy_id INT PRIMARY KEY, 
            vacancy_name VARCHAR(100) NOT NULL, 
            salary_from REAL, 
            salary_to REAL, 
            currency VARCHAR(5) NOT NULL,
            published_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP NOT NULL,
            url VARCHAR(200),
            alternate_url VARCHAR(200),
            employer_id INT
            );

            CREATE TABLE employers (
            employer_id INT PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL, 
            url VARCHAR(100) NOT NULL,
            alternate_url VARCHAR(100) NOT NULL,
            logo_urls TEXT NOT NULL,
            accredited_it_employer BOOL 
             );
             

            """)
        # временная таблица для промежуточного хранения данных по компаниям
        cursor.execute(f""" 
                        CREATE TEMP TABLE temp_employers(
                        employer_id INT NOT NULL,
                        company_name VARCHAR(100) NOT NULL, 
                        url VARCHAR(100) NOT NULL,
                        alternate_url VARCHAR(100) NOT NULL,
                        logo_urls TEXT NOT NULL,
                        accredited_it_employer BOOL );
                        """)
        cursor.close()
        conn.commit()
        conn.close()
