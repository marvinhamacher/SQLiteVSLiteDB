import logging
import sqlite3
import threading
from pathlib import Path

from connectors.base import Connector


logger = logging.getLogger(__name__)


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
        logger.info("SQLite connector initialized: db=%s", self.db_path)

    def _initialize_database(self):
        with sqlite3.connect(str(self.db_path)) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("""
                CREATE TABLE IF NOT EXISTS benchmark (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    value INTEGER,
                    category TEXT
                )
            """)

            db.commit()

        logger.debug("SQLite schema initialized: db=%s", self.db_path)

    def _get_connection(self):
        if not hasattr(self._local, "db"):
            self._local.db = sqlite3.connect(
                str(self.db_path)
            )

            self._local.cursor = self._local.db.cursor()
            logger.debug(
                "SQLite connection created: thread=%s conn=%s",
                threading.get_ident(),
                id(self._local.db),
            )

        return self._local.db, self._local.cursor

    def insert(self, data):
        db, cursor = self._get_connection()
        record_id = data["id"]

        try:
            cursor.execute(
                """
                INSERT INTO benchmark
                (id, name, value, category)
                VALUES (?, ?, ?, ?)
                """,
                (
                    record_id,
                    data["name"],
                    data["value"],
                    data["category"]
                )
            )

            if not getattr(self._local, "in_transaction", False):
                db.commit()

            logger.debug("SQLite INSERT id=%s", record_id)
            return True

        except Exception:
            if not getattr(self._local, "in_transaction", False):
                db.rollback()
            logger.exception("SQLite INSERT failed: id=%s", record_id)
            raise

    def find_all(self):
        _, cursor = self._get_connection()

        cursor.execute(
            "SELECT * FROM benchmark"
        )

        result = cursor.fetchall()
        logger.debug("SQLite SELECT all: rows=%s", len(result))
        return result

    def find_by_id(self, record_id):
        _, cursor = self._get_connection()

        cursor.execute(
            "SELECT * FROM benchmark WHERE id = ?",
            (record_id,)
        )

        result = cursor.fetchone()
        logger.debug(
            "SQLite SELECT id=%s: found=%s",
            record_id,
            result is not None,
        )
        return result

    def update(self, data):
        db, cursor = self._get_connection()
        record_id = data["id"]

        try:
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
                    record_id
                )
            )

            db.commit()
            changed = cursor.rowcount > 0
            logger.debug("SQLite UPDATE id=%s changed=%s", record_id, changed)
            return changed

        except Exception:
            db.rollback()
            logger.exception("SQLite UPDATE failed: id=%s", record_id)
            raise

    def delete(self, record_id):
        db, cursor = self._get_connection()

        try:
            cursor.execute(
                "DELETE FROM benchmark WHERE id = ?",
                (record_id,)
            )
            db.commit()
            changed = cursor.rowcount > 0
            logger.debug("SQLite DELETE id=%s changed=%s", record_id, changed)
            return changed

        except Exception:
            db.rollback()
            logger.exception("SQLite DELETE failed: id=%s", record_id)
            raise

    def count(self):
        _, cursor = self._get_connection()

        cursor.execute(
            "SELECT COUNT(*) FROM benchmark"
        )

        result = cursor.fetchone()[0]
        logger.debug("SQLite COUNT=%s", result)
        return result

    def begin_transaction(self):
        _, cursor = self._get_connection()
        self._local.in_transaction = True
        cursor.execute("BEGIN")
        logger.debug("SQLite transaction BEGIN: thread=%s", threading.get_ident())

    def commit(self):
        db, _ = self._get_connection()

        db.commit()
        self._local.in_transaction = False
        logger.debug("SQLite transaction COMMIT: thread=%s", threading.get_ident())

    def rollback(self):
        db, _ = self._get_connection()
        db.rollback()
        self._local.in_transaction = False
        logger.debug("SQLite transaction ROLLBACK: thread=%s", threading.get_ident())

    def close(self):
        if hasattr(self._local, "db"):
            self._local.db.close()

            del self._local.db
            del self._local.cursor
            logger.debug("SQLite connection closed: thread=%s", threading.get_ident())
