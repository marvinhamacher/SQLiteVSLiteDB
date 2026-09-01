# TODO: Quasi die Main des Benchmarking tools
import timeit

from services.reportmanagement import ReportService
from services.benchmarkgroups import *
from services.environmentservice import EnvironmentService

ITERATIONS = 5
sqlite = InjectableBenchmark(SQLiteConnector())
litedb = InjectableBenchmark(LiteDBConnector())


def start_benchmark():
    user = input("Testkürzel aus der Excel eingeben: ")
    env_service = EnvironmentService()
    env_service.verify_configuration()
    config = env_service.gather_system_information()
    rep_service = ReportService(config, user)
    for i in range(ITERATIONS):
        sqlite_res = []
        sqlite_time = timeit.timeit(
            lambda: sqlite_res.append(sqlite.run_test()),
            number=1
        ) * 1000

        sqlite_res = sqlite_res[0]

        litedb_res = []
        litedb_time = timeit.timeit(
            lambda: litedb_res.append(litedb.run_test()),
            number=1
        ) * 1000

        litedb_res = litedb_res[0]

        rep_service.append_results(
            exec_time={
                "sqlite": sqlite_time,
                "litedb": litedb_time
            },
            results={
                "sqlite": sqlite_res,
                "litedb": litedb_res
            },
            iteration_nr=i + 1
        )
