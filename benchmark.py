#TODO: Quasi die Main des Benchmarking tools

def start_benchmark:
  sqlite = SQLiteBenchmark()
  litedb = LiteDBBenchmark()
  sqlite.run()
  litedb.run()
  return
