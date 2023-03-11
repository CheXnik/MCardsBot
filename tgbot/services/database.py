from typing import Any

import arrow
import pymysql as pymysql


class DataBase:
    """ Клас для взаємодії з базою даних  """
    def __init__(self, host: str, user: str, password: str, name_database: str, port: int = 3306):
        self.host = host
        self.user = user
        self.password = password
        self.name_database = name_database
        self.port = port

    def __execute_query(self, query: str, values: Any = None) -> tuple[tuple[Any, ...], ...]:
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.password,
                               database=self.name_database,
                               charset='utf8mb4')
        cur = conn.cursor()
        cur.execute(query, values)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def check_user(self, user_tg_id: int | str) -> bool:
        """ Перевірки чи є користувач в базі даних """
        user = self.__execute_query('select * from Users where user_tg_id=%s;', user_tg_id)
        return True if user else False

    def add_user(self, user_tg_id: int | str):
        """ Додавання користувача в базу даних """
        if not self.check_user(user_tg_id):
            date = arrow.get(arrow.now()).format('YYYY-MM-DD')
            self.__execute_query('INSERT INTO Users (user_tg_id, register_date) VALUES (%s, %s);', (user_tg_id, date))

    def add_card(self, user_tg_id: int | str, title: str, number: str, service_name: str):
        """ Додавання карти/гаманця в базу даних """
        logo_id = self.get_logo_id_by_logo_name(service_name)

        if not logo_id:
            return False
        else:
            self.__execute_query('INSERT INTO Cards (user_tg_id, title, number, logo) '
                                 'VALUES (%s, %s, %s, %s);', (user_tg_id, title, number, logo_id))
            return True

    def get_card(self, user_tg_id: int | str, card_id) -> tuple:
        """ Додавання карти/гаманця користувача в базу даних """
        return self.__execute_query('SELECT Cards.id, Cards.title, Cards.number, Logos.url '
                                    'FROM Cards '
                                    'INNER JOIN Logos ON Cards.logo=Logos.id '
                                    'WHERE user_tg_id = %s AND Cards.id = %s;', (user_tg_id, card_id))[0]

    def get_all_cards(self, user_tg_id: int | str):
        """ Отримання всіх карткок/гаманеців користувача з бази даних """
        return self.__execute_query('SELECT Cards.id, Cards.title, Cards.number, Logos.url '
                                    'FROM Cards '
                                    'INNER JOIN Logos ON Cards.logo=Logos.id '
                                    'WHERE user_tg_id = %s;', user_tg_id)

    def add_logo(self):
        """ Додавання логотипа в базу даних """
        ...

    def get_all_logos(self):
        """ Отримання всіх логотипів користувача з бази даних """
        return self.__execute_query('SELECT id, name, file_id FROM Logos')

    def get_logo_id_by_logo_name(self, service_name: str) -> int | bool:
        """ Отримання логотипа з бази даних """
        logo_id = self.__execute_query('SELECT id FROM Logos WHERE name = %s;', service_name)
        return logo_id[0][0] if logo_id else False

    def update_card_title(self, card_id: int | str, card_title: str):
        """ Оновлення назви картки/гаманця в базі даних """
        self.__execute_query('UPDATE Cards SET title = %s WHERE id = %s;', (card_title, card_id))

    def update_card_number(self, card_id: int | str, card_number: str):
        """ Оновлення номера картки/гаманця в базі даних """
        self.__execute_query('UPDATE Cards SET number = %s WHERE id = %s;', (card_number, card_id))

    def update_card_logo(self, card_id: int | str, service_name: str):
        """ Оновлення логотипу картки/гаманця в базі даних """
        logo_id = self.get_logo_id_by_logo_name(service_name)
        self.__execute_query('UPDATE Cards SET logo = %s WHERE id = %s;', (logo_id, card_id))

    def delete_card(self, card_id: int | str):
        """ Видалення картки/гаманця картки з бази даних """
        self.__execute_query('DELETE FROM Cards WHERE id = %s;', card_id)
