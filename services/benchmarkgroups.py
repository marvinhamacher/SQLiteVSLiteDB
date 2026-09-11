from abc import abstractmethod, ABC

from connectors.base import Connector
from testcases.delete_test import DeleteTest
from testcases.insert_test import InsertTest
from testcases.select_test import SelectTest
from testcases.transcation_test import TransactionTest
from testcases.update_test import UpdateTest


class Benchmark(ABC):
    results = [{}, {}, {}]
    concurrency_levels = [
        1,
        2,
        4,
        8,
        16
    ]

    @abstractmethod
    def run_test(self):
        res_latency = self.results[0]
        res_queryrate = self.results[1]
        res_tps = self.results[2]
        return {
            "tps": res_tps,
            "queryrate": res_queryrate,
            "latency": res_latency
        }


class InjectableBenchmark(Benchmark):

    def __init__(self, db_driver: Connector):
        super().__init__()

        self.database = db_driver

        self.insertTest = InsertTest(
            self.database
        )

        self.deleteTest = DeleteTest(
            self.database
        )

        self.selectTest = SelectTest(
            self.database
        )

        self.updateTest = UpdateTest(
            self.database
        )

        self.transaction = TransactionTest(
            self.database
        )

    def run_test(self):
        for concurrency in self.concurrency_levels:
            insert_result = self.insertTest.run(
                amount=1000,
                concurrency=concurrency
            )

            delete_result = self.deleteTest.run(
                amount=1000,
                concurrency=concurrency
            )

            select_result = self.selectTest.run(
                amount=1000,
                concurrency=concurrency
            )

            update_result = self.updateTest.run(
                amount=1000,
                concurrency=concurrency
            )

            transaction_result = self.transaction.run(
                amount=1000,
                concurrency=concurrency
            )

            self.results[0][concurrency] = {
                "insert": insert_result["latency"],
                "delete": delete_result["latency"],
                "select": select_result["latency"],
                "update": update_result["latency"],
                "transaction": transaction_result["latency"]
            }

            self.results[1][concurrency] = {
                "insert": insert_result["query_rate"],
                "delete": delete_result["query_rate"],
                "select": select_result["query_rate"],
                "update": update_result["query_rate"],
                "transaction": transaction_result["query_rate"]
            }

            self.results[2][concurrency] = {
                "insert": insert_result.get("tps", 0),
                "delete": delete_result.get("tps", 0),
                "select": select_result.get("tps", 0),
                "update": update_result.get("tps", 0),
                "transaction": transaction_result.get("tps", 0)
            }

        return super().run_test()

    def close(self):
        self.database.close()
