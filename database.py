import sqlite3
from datetime import datetime

DB_NAME = "data.db"


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            site TEXT,
            model TEXT,
            name TEXT,
            url TEXT,

            inventory INTEGER,
            availability TEXT,
            button_status TEXT,
            price INTEGER,

            first_seen TEXT,
            last_seen TEXT,
            last_notify TEXT
        )
        """)
        self.conn.commit()

    def get_product(self, product_id):
        cursor = self.conn.execute(
            "SELECT * FROM products WHERE id=?",
            (product_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    def save_product(self, product):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        old = self.get_product(product["id"])

        if old is None:

            self.conn.execute("""
            INSERT INTO products(
                id,
                site,
                model,
                name,
                url,
                inventory,
                availability,
                button_status,
                price,
                first_seen,
                last_seen,
                last_notify
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """, (

                product["id"],
                product["site"],
                product["model"],
                product["name"],
                product["url"],

                product["inventory"],
                product["availability"],
                product["button_status"],
                product["price"],

                now,
                now,
                None

            ))

        else:

            self.conn.execute("""
            UPDATE products
            SET
                site=?,
                model=?,
                name=?,
                url=?,

                inventory=?,
                availability=?,
                button_status=?,
                price=?,

                last_seen=?
            WHERE id=?
            """, (

                product["site"],
                product["model"],
                product["name"],
                product["url"],

                product["inventory"],
                product["availability"],
                product["button_status"],
                product["price"],

                now,
                product["id"]

            ))

        self.conn.commit()

    def update_notify_time(self, product_id):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.conn.execute(
            "UPDATE products SET last_notify=? WHERE id=?",
            (now, product_id)
        )

        self.conn.commit()

    def need_notify(self, old, new):

        if old is None:
            return True, "new"

        if old["inventory"] == 0 and new["inventory"] == 1:
            return True, "restock"

        return False, ""

    def close(self):
        self.conn.close()