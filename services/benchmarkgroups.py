from abc import abstractmethod, ABC


class Benchmark(ABC):
    @abstractmethod
    def test_latency(self):
        pass

    @abstractmethod
    def test_queryrate(self):
        pass

    @abstractmethod
    def test_tps(self):
        pass

    @abstractmethod
    def run_test(self):
        res_latency = self.test_queryrate()
        res_queryrate = self.test_queryrate()
        res_tps = self.test_queryrate()
        return {
            "tps": res_tps,
            "queryrate": res_queryrate,
            "latency": res_latency
        }


class LiteDBBenchmark(Benchmark):
    def test_latency(self):
        pass

    def test_queryrate(self):
        pass

    def test_tps(self):
        pass

    def run_test(self):
        super().run_test()


class SQLiteBenchmark(Benchmark):
    def test_latency(self):
        pass

    def test_queryrate(self):
        pass

    def test_tps(self):
        pass

    def run_test(self):
        super().run_test()
