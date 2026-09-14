from abc import ABC, abstractmethod

from connectors.base import Connector
from testcases.delete_test import DeleteTest
from testcases.insert_test import InsertTest
from testcases.select_test import SelectTest
from testcases.transcation_test import TransactionTest
from testcases.update_test import UpdateTest


class Benchmark(ABC):

    concurrency_levels = [1, 2, 4, 8, 16]

    @abstractmethod
    def run_test(self):
        pass


class InjectableBenchmark(Benchmark):

    def __init__(self, db_driver: Connector):
        self.database = db_driver

        self.insert_test = InsertTest(self.database)
        self.delete_test = DeleteTest(self.database)
        self.select_test = SelectTest(self.database)
        self.update_test = UpdateTest(self.database)
        self.transaction_test = TransactionTest(self.database)

    @staticmethod
    def _per_second(result):
        duration_seconds = result["duration_ms"] / 1000

        if duration_seconds <= 0:
            return 0

        return result["queries_sent"] / duration_seconds

    @staticmethod
    def _transactions_per_second(result):
        duration_seconds = result["duration_ms"] / 1000

        if duration_seconds <= 0:
            return 0

        return result["successful"] / duration_seconds

    def run_test(self):
        latency_results = {}
        queryrate_results = {}
        tps_results = {}

        for concurrency in self.concurrency_levels:

            print(f"insert {concurrency}")
            insert_result = self.insert_test.run(
                amount=1000,
                concurrency=concurrency,
            )

            print(f"select {concurrency}")
            select_result = self.select_test.run(
                amount=1000,
                concurrency=concurrency,
            )

            print(f"update {concurrency}")
            update_result = self.update_test.run(
                amount=1000,
                concurrency=concurrency,
            )

            print(f"transaction {concurrency}")
            transaction_result = self.transaction_test.run(
                amount=1000,
                concurrency=concurrency,
            )

            print(f"delete {concurrency}")
            delete_result = self.delete_test.run(
                amount=1000,
                concurrency=concurrency,
            )

            latency_results[concurrency] = {
                "insert": insert_result["latency"],
                "select": select_result["latency"],
                "update": update_result["latency"],
                "transaction": transaction_result["latency"],
                "delete": delete_result["latency"],
            }

            queryrate_results[concurrency] = {
                "insert": self._per_second(insert_result),
                "select": self._per_second(select_result),
                "update": self._per_second(update_result),
                "transaction": self._per_second(transaction_result),
                "delete": self._per_second(delete_result),
            }

            tps_results[concurrency] = {
                "successful_transactions_per_second": (
                    self._transactions_per_second(transaction_result)
                )
            }

        return {
            "tps": tps_results,
            "queryrate": queryrate_results,
            "latency": latency_results,
        }

    def close(self):
        self.database.close()