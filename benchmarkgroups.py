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
    pass



ITERATIONS = 5
class LiteDBBenchmark(Benchmark):
  def test_latency(self):
    pass

  def test_queryrate(self):
    pass
    
  def test_tps(self):
    pass

  def run_test(self):
    pass


class SQLiteBenchmark(Benchmark):
  def test_latency(self):
    pass

  def test_queryrate(self):
    pass
    
  def test_tps(self):
    pass

  def run_test(self):
    pass

