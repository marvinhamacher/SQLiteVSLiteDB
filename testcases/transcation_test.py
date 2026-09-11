import uuid
from time import perf_counter

from testcases.base import BaseTest


class TransactionTest(BaseTest):

    OPERATIONS_PER_TRANSACTION = 10

    def run_operation(self, transaction_id):

        start = perf_counter()

        self.database.begin_transaction()

        try:
            for i in range(self.OPERATIONS_PER_TRANSACTION):

                record_id = str(uuid.uuid4())
                self.database.insert({
                    "id": record_id,
                    "name": f"Transaction {transaction_id}",
                    "value": i,
                    "category": "transaction"
                })

            self.database.commit()

        except Exception:
            self.database.rollback()
            raise

        elapsed = (
            perf_counter() - start
        ) * 1000

        return {
            "latency_ms": elapsed
        }