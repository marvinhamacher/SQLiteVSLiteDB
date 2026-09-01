from time import perf_counter

from testcases.base import BaseTest


class InsertTest(BaseTest):

    def run_operation(self, index):
        data = {
            "id": index,
            "name": f"User {index}",
            "value": index,
            "category": "benchmark"
        }

        start = perf_counter()

        self.database.insert(data)

        elapsed = (
            perf_counter() - start
        ) * 1000

        return {
            "latency_ms": elapsed
        }
