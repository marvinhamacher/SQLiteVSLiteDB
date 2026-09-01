from time import perf_counter

from testcases.base import BaseTest


class UpdateTest(BaseTest):

    def run_operation(self, index):

        data = {
            "id": index,
            "name": f"Updated User {index}",
            "value": index + 1,
            "category": "updated"
        }

        start = perf_counter()

        self.database.update(data)

        elapsed = (
            perf_counter() - start
        ) * 1000

        return {
            "latency_ms": elapsed
        }