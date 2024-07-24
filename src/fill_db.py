import psycopg2
from src.utils import get_id_employees
from src.utils import get_vacancies
from src.settings import COMPANY_NAMES, EMPLOYEE_API, VACANCIES_API


def data_fill(database_name: str, params: dict) -> None:
    """
    Ввод данныз в БД
    :param database_name:
    :param params:
    :return:
    """

    # получение id компаний по их названиям
    id_employees_list = get_id_employees(COMPANY_NAMES, EMPLOYEE_API)
    # получение вакансий для каждой из выбранных компаний-работодателей
    get_vacancy_list = get_vacancies(id_employees_list, VACANCIES_API)

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    # cur = conn.cursor()
    with conn.cursor() as cur:
        # временная таблица для промежуточного хранения данных по компаниям
        cur.execute(f""" 
                        CREATE TEMP TABLE temp_employers(
                        employer_id INT NOT NULL,
                        company_name VARCHAR(100) NOT NULL, 
                        url VARCHAR(100) NOT NULL,
                        alternate_url VARCHAR(100) NOT NULL,
                        logo_urls TEXT NOT NULL,
                        accredited_it_employer BOOL );
                        """)
        for company_vacancies in get_vacancy_list:  # Список компаний
            for vacancy in company_vacancies:  # Список вакансий по каждой отдельной компании
                add_vacancy = (
                    vacancy['id'], vacancy['name'], vacancy['salary']['from'] if vacancy.get('salary') else 0,
                    vacancy['salary']['to'] if vacancy.get('salary') else 0,
                    vacancy['salary']['currency'] if vacancy.get('salary') else '', vacancy['published_at'],
                    vacancy['created_at'], vacancy['url'], vacancy['alternate_url'],
                    vacancy['employer']['id'])

                add_employer = (
                    vacancy['employer'].get('id'),
                    vacancy['employer'].get('name'),
                    vacancy['employer'].get('url'),
                    vacancy['employer'].get('alternate_url'),
                    str(vacancy['employer'].get('logo_urls')),
                    vacancy['employer'].get('accredited_it_employer')
                )
                #  добавляем данные в таблицы

                cur.execute(f"""
                                        INSERT INTO vacancies(vacancy_id, vacancy_name, salary_from, 
                                        salary_to, currency, published_at, created_at, url, alternate_url, 
                                        employer_id) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning *;""",
                            add_vacancy)

            cur.execute(f"""
                                    INSERT INTO temp_employers
                                    (employer_id, -- vacancy_id, 
                                    company_name, url, 
                                    alternate_url, logo_urls, -- vacancies_url, 
                                    accredited_it_employer) VALUES 
                                    (%s, %s, %s, %s, %s, %s) returning *;
                        """, add_employer)

        cur.execute(f"""
                INSERT INTO employers
                SELECT DISTINCT * FROM temp_employers """)

        cur.execute(f"""DROP TABLE  temp_employers""")

        cur.execute(f"""ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers 
        FOREIGN KEY(employer_id) REFERENCES employers(employer_id);""")

        conn.commit()
        cur.close()
    print("База данных создана, данные в БД загружены.")
    conn.close()
