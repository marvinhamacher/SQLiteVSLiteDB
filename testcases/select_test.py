from time import perf_counter

from testcases.base import BaseTest


class SelectTest(BaseTest):

    def run_operation(self, index):

        start = perf_counter()

        result = self.database.find_by_id(index)

        elapsed = (
            perf_counter() - start
        ) * 1000

        return {
            "latency_ms": elapsed,
            "result": result
        }