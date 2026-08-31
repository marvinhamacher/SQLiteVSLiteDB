import sqlite3
from pathlib import Path


class SQLiteConnector:

    def __init__(self):
        root = Path(__file__).resolve().parent.parent

        db_path = root / "resources" / "DB" / "sqlite.db"

        db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.db = sqlite3.connect(str(db_path))

        self.cursor = self.db.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value INTEGER,
                category TEXT
            )
        """)

        self.db.commit()

    def insert(self, data):
        self.cursor.execute(
            """
            INSERT INTO benchmark
            (id, name, value, category)
            VALUES (?, ?, ?, ?)
            """,
            (
                data["id"],
                data["name"],
                data["value"],
                data["category"]
            )
        )

        self.db.commit()

        return True

    def find_all(self):
        self.cursor.execute(
            "SELECT * FROM benchmark"
        )

        return self.cursor.fetchall()

    def find_by_id(self, record_id):
        self.cursor.execute(
            "SELECT * FROM benchmark WHERE id = ?",
            (record_id,)
        )

        return self.cursor.fetchone()

    def update(self, data):
        self.cursor.execute(
            """
            UPDATE benchmark
            SET name = ?,
                value = ?,
                category = ?
            WHERE id = ?
            """,
            (
                data["name"],
                data["value"],
                data["category"],
                data["id"]
            )
        )

        self.db.commit()

        return self.cursor.rowcount > 0

    def delete(self, record_id):
        self.cursor.execute(
            "DELETE FROM benchmark WHERE id = ?",
            (record_id,)
        )

        self.db.commit()

        return self.cursor.rowcount > 0

    def count(self):
        self.cursor.execute(
            "SELECT COUNT(*) FROM benchmark"
        )

        return self.cursor.fetchone()[0]

    def begin_transaction(self):
        self.cursor.execute("BEGIN")

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()