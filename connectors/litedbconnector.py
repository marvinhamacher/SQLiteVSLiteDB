from pathlib import Path
import clr


class LiteDBConnector:

    def __init__(self):
        root = Path(__file__).resolve().parent.parent

        dll_path = root / "resources" / "lib" / "LiteDB.dll"
        db_path = root / "resources" / "DB" / "litedb.db"

        db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        clr.AddReference(str(dll_path))

        from LiteDB import LiteDatabase

        self.db = LiteDatabase(str(db_path))
        self.collection = self.db.GetCollection("benchmark")

    def insert(self, data):
        return self.collection.Insert(data)

    def find_all(self):
        return list(self.collection.FindAll())

    def find_by_id(self, record_id):
        return self.collection.FindById(record_id)

    def update(self, data):
        return self.collection.Update(data)

    def delete(self, record_id):
        return self.collection.Delete(record_id)

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