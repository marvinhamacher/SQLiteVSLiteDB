from pathlib import Path

import clr

from connectors.base import Connector


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
        return self.collection.Insert(
            self._to_document(data)
        )

    def find_all(self):
        return list(
            self.collection.FindAll()
        )

    def find_by_id(self, record_id):
        return self.collection.FindById(
            self._to_bson(record_id)
        )

    def update(self, data):
        return self.collection.Update(
            self._to_document(data)
        )

    def delete(self, record_id):
        return self.collection.Delete(
            self._to_bson(record_id)
        )

    def count(self):
        return self.collection.Count()

    def begin_transaction(self):
        return self.db.BeginTrans()

    def commit(self):
        return self.db.Commit()

    def rollback(self):
        return self.db.Rollback()

    def close(self):
        self.db.Dispose()