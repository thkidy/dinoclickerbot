import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def add_user(self, user_id, first_name, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT INTO users (user_id, first_name, referrer_id) VALUES (?,?, ?)", (user_id, first_name, referrer_id,))
            else:
                return self.cursor.execute("INSERT INTO users (user_id, first_name) VALUES (?, ?)", (user_id, first_name,))

    async def increment_user_clicks(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET clicks = clicks + 1 WHERE user_id = ?", (user_id,))

    async def get_user_clicks(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT clicks FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None

    async def count_score(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT clicks FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def count_referals(self,user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(id) as count FROM users WHERE referrer_id = ?", (user_id,)).fetchone()[0]

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM users").fetchall()

    def count_active_users(self):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM users WHERE active = 1").fetchone()

    def count_unactive_users(self):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM users WHERE active = 0").fetchone()

# получение ID реферрера
    def get_referrer(self, user_id):
        with self.connection:
            referrer = self.cursor.execute("SELECT referrer_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return referrer[0] if referrer else None

# 10% от реферала
    async def reward_referrer_with_percentage(self, referrer_id, referral_clicks):
        with self.connection:
            referrer_clicks = await self.get_user_clicks(referrer_id)
            if referrer_clicks is None:
                referrer_clicks = 0
            bonus_clicks = round(referral_clicks * 0.1, 1)
            new_referrer_clicks = round(referrer_clicks + bonus_clicks, 1)
            self.cursor.execute("UPDATE users SET clicks = ? WHERE user_id = ?", (new_referrer_clicks, referrer_id))
            self.connection.commit()

# +500 от реферала
    def reward_referrer(self, referrer_id):
        with self.connection:
            current_clicks = self.cursor.execute("SELECT clicks FROM users WHERE user_id = ?", (referrer_id,)
            ).fetchone()
            if current_clicks is None:
                current_clicks = 0
            else:
                current_clicks = current_clicks[0]
            new_clicks = current_clicks + 500
            self.cursor.execute("UPDATE users SET clicks = ? WHERE user_id = ?",(new_clicks, referrer_id))
            self.connection.commit()

    def get_task_data(self):
        with self.connection:
            result = self.cursor.execute("SELECT channels, task_message FROM tasks").fetchone()
        return result

    def update_task_data(self, channels, task_message):
        with self.connection:
            return self.cursor.execute("UPDATE tasks SET channels = ?, task_message = ?", (channels, task_message))

    async def add_coins(self, user_id, amount):
        with self.connection:
            return self.cursor.execute("UPDATE users SET clicks = clicks + ? WHERE user_id = ?", (amount, user_id,))

    def get_task_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT task_completed FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return result[0] == 1

    async def set_task_completed(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET task_completed = 1 WHERE user_id = ?", (user_id,))

    async def reset_task_status_for_all_users(self):
        with self.connection:
            return self.cursor.execute("UPDATE users SET task_completed = 0")