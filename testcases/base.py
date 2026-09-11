from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter


class BaseTest(ABC):

    def __init__(self, database):
        self.database = database

    @abstractmethod
    def run_operation(self, index):
        pass

    def run(self, amount=1000, concurrency=1):
        start = perf_counter()

        successful = 0
        failed = 0
        latencies = []

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [
                executor.submit(self.run_operation, index)
                for index in range(amount)
            ]

            for future in as_completed(futures):
                try:
                    result = future.result()

                    successful += 1
                    latencies.append(result["latency_ms"])

                except Exception:
                    failed += 1

        duration_ms = (perf_counter() - start) * 1000

        avg_latency = (
            sum(latencies) / len(latencies)
            if latencies
            else 0
        )

        return {
            "queries_sent": amount,
            "successful": successful,
            "failed": failed,
            "duration_ms": duration_ms,
            "latency": {
                "avg_ms": avg_latency,
                "min_ms": min(latencies) if latencies else 0,
                "max_ms": max(latencies) if latencies else 0,
            },
        }