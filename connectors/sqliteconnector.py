import sqlite3
import threading
from pathlib import Path

from connectors.base import Connector


class SQLiteConnector(Connector):

    def __init__(self):
        root = Path(__file__).resolve().parent.parent

        self.db_path = root / "resources" / "DB" / "sqlite.db"

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._local = threading.local()

        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(str(self.db_path)) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS benchmark (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    value INTEGER,
                    category TEXT
                )
            """)

            db.commit()

    def _get_connection(self):
        if not hasattr(self._local, "db"):
            self._local.db = sqlite3.connect(
                str(self.db_path)
            )

            self._local.cursor = self._local.db.cursor()

        return self._local.db, self._local.cursor

    def insert(self, data):
        db, cursor = self._get_connection()

        cursor.execute(
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

        if not getattr(self._local, "in_transaction", False):
            db.commit()

        return True

    def find_all(self):
        _, cursor = self._get_connection()

        cursor.execute(
            "SELECT * FROM benchmark"
        )

        return cursor.fetchall()

    def find_by_id(self, record_id):
        _, cursor = self._get_connection()

        cursor.execute(
            "SELECT * FROM benchmark WHERE id = ?",
            (record_id,)
        )

        return cursor.fetchone()

    def update(self, data):
        db, cursor = self._get_connection()

        cursor.execute(
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

        db.commit()

        return cursor.rowcount > 0

    def delete(self, record_id):
        db, cursor = self._get_connection()

        cursor.execute(
            "DELETE FROM benchmark WHERE id = ?",
            (record_id,)
        )

        db.commit()

        return cursor.rowcount > 0

    def count(self):
        _, cursor = self._get_connection()

        cursor.execute(
            "SELECT COUNT(*) FROM benchmark"
        )

        return cursor.fetchone()[0]

    def begin_transaction(self):
        _, cursor = self._get_connection()
        self._local.in_transaction = True
        cursor.execute("BEGIN")

    def commit(self):
        db, _ = self._get_connection()

        db.commit()
        self._local.in_transaction = False

    def rollback(self):
        db, _ = self._get_connection()

        db.rollback()

    def close(self):
        if hasattr(self._local, "db"):
            self._local.db.close()

            del self._local.db
            del self._local.cursor