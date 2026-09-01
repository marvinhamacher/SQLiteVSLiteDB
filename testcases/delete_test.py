from time import perf_counter

from testcases.base import BaseTest


class DeleteTest(BaseTest):

    def run_operation(self, index):

        start = perf_counter()

        self.database.delete(index)

        elapsed = (
            perf_counter() - start
        ) * 1000

        return {
            "latency_ms": elapsed
        }