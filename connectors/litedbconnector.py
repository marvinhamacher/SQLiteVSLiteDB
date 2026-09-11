import logging
from pathlib import Path

import clr

from connectors.base import Connector


logger = logging.getLogger(__name__)


class LiteDBConnector(Connector):

    def __init__(self):
        root = Path(__file__).resolve().parent.parent

        dll_path = root / "resources" / "lib" / "LiteDB.dll"
        db_path = root / "resources" / "DB" / "litedb.db"

        db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        clr.AddReference(str(dll_path))

        from LiteDB import (
            LiteDatabase,
            BsonDocument,
            BsonValue,
            BsonArray,
            BsonAutoId,
            BsonMapper,
        )

        self.BsonDocument = BsonDocument
        self.BsonValue = BsonValue
        self.BsonArray = BsonArray

        self.mapper = BsonMapper.Global

        self.db = LiteDatabase(
            str(db_path),
            self.mapper,
        )

        self.collection = self.db.GetCollection(
            "benchmark",
            BsonAutoId.ObjectId
        )

        logger.info("LiteDB connector initialized: db=%s", db_path)

    def _to_bson(self, value):
        if isinstance(value, self.BsonDocument):
            return value

        if value is None:
            return self.BsonValue()

        if isinstance(value, bool):
            return self.BsonValue(value)

        if isinstance(value, int):
            return self.BsonValue(value)

        if isinstance(value, float):
            return self.BsonValue(value)

        if isinstance(value, str):
            return self.BsonValue(value)

        if isinstance(value, dict):
            document = self.BsonDocument()

            for key, item in value.items():
                document[str(key)] = self._to_bson(item)

            return document

        if isinstance(value, (list, tuple)):
            array = self.BsonArray()

            for item in value:
                array.Add(self._to_bson(item))

            return array

        raise TypeError(
            f"Unsupported value for LiteDB BSON conversion: "
            f"{type(value).__name__}"
        )

    def _to_document(self, data):
        document = self.BsonDocument()
        for key, value in data.items():
            if key == "id":
                document["_id"] = self._to_bson(value)
            else:
                document[str(key)] = self._to_bson(value)

        return document

    def insert(self, data):
        record_id = data["id"]

        try:
            result = self.collection.Insert(
                self._to_document(data)
            )
            logger.debug("LiteDB INSERT id=%s", record_id)
            return result
        except Exception:
            logger.exception("LiteDB INSERT failed: id=%s", record_id)
            raise

    def find_all(self):
        try:
            result = list(self.collection.FindAll())
            logger.debug("LiteDB SELECT all: rows=%s", len(result))
            return result
        except Exception:
            logger.exception("LiteDB SELECT all failed")
            raise

    def find_by_id(self, record_id):
        try:
            result = self.collection.FindById(
                self._to_bson(record_id)
            )
            logger.debug(
                "LiteDB SELECT id=%s: found=%s",
                record_id,
                result is not None,
            )
            return result
        except Exception:
            logger.exception("LiteDB SELECT failed: id=%s", record_id)
            raise

    def update(self, data):
        record_id = data["id"]

        try:
            result = self.collection.Update(
                self._to_document(data)
            )
            logger.debug("LiteDB UPDATE id=%s result=%s", record_id, result)
            return result
        except Exception:
            logger.exception("LiteDB UPDATE failed: id=%s", record_id)
            raise

    def delete(self, record_id):
        try:
            result = self.collection.Delete(
                self._to_bson(record_id)
            )
            logger.debug("LiteDB DELETE id=%s result=%s", record_id, result)
            return result
        except Exception:
            logger.exception("LiteDB DELETE failed: id=%s", record_id)
            raise

    def count(self):
        try:
            result = self.collection.Count()
            logger.debug("LiteDB COUNT=%s", result)
            return result
        except Exception:
            logger.exception("LiteDB COUNT failed")
            raise

    def begin_transaction(self):
        try:
            result = self.db.BeginTrans()
            logger.debug("LiteDB transaction BEGIN")
            return result
        except Exception:
            logger.exception("LiteDB transaction BEGIN failed")
            raise

    def commit(self):
        try:
            result = self.db.Commit()
            logger.debug("LiteDB transaction COMMIT")
            return result
        except Exception:
            logger.exception("LiteDB transaction COMMIT failed")
            raise

    def rollback(self):
        try:
            result = self.db.Rollback()
            logger.debug("LiteDB transaction ROLLBACK")
            return result
        except Exception:
            logger.exception("LiteDB transaction ROLLBACK failed")
            raise

    def close(self):
        self.db.Dispose()
        logger.debug("LiteDB connection closed")
