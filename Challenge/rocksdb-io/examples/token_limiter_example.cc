#include <cassert>
#include <iostream>
#include <memory>
#include <string>

#include "rocksdb/db.h"
#include "rocksdb/env.h"
#include "rocksdb/options.h"
#include "rocksdb/slice.h"
#include "rocksdb/table.h"
#include "util/token_limiter.h"

using namespace rocksdb;
std::string kDBPath = "/tmp/rocksdb_token_limiter_example";

int main() {
  DB* db;
  Options options;
  // Optimize RocksDB. This is the easiest way to get RocksDB to perform well
  options.IncreaseParallelism();
  options.OptimizeLevelStyleCompaction();
  // create the DB if it's not already present
  options.create_if_missing = true;
  options.use_direct_reads = true;
  options.use_direct_io_for_flush_and_compaction = true;

  BlockBasedTableOptions table_options;
  table_options.no_block_cache = true;
  options.table_factory.reset(NewBlockBasedTableFactory(table_options));

  ReadOptions read_options;

  // init token limiter
  TokenLimiter::SetDefaultInstance(
      std::unique_ptr<TokenLimiter>(new TokenLimiter(3000)));

  // open DB
  Status s = DB::Open(options, kDBPath, &db);
  assert(s.ok());

  TokenLimiter::PrintStatus();

  std::string value;
  db->Get(read_options, "key10000", &value);

  TokenLimiter::PrintStatus();

  // // Put key-value
  // s = db->Put(WriteOptions(), "key1", "value");
  // assert(s.ok());
  // std::string value;
  // // get value
  // s = db->Get(ReadOptions(Env::IO_SRC_USER), "key1", &value);
  // assert(s.ok());
  // assert(value == "value");

  // // atomically apply a set of updates
  // {
  //   WriteBatch batch;
  //   batch.Delete("key1");
  //   batch.Put("key2", value);
  //   s = db->Write(WriteOptions(), &batch);
  // }

  // s = db->Get(ReadOptions(Env::IO_SRC_USER), "key1", &value);
  // assert(s.IsNotFound());

  // db->Get(ReadOptions(Env::IO_SRC_USER), "key2", &value);
  // assert(value == "value");

  // {
  //   PinnableSlice pinnable_val;
  //   db->Get(ReadOptions(Env::IO_SRC_USER), db->DefaultColumnFamily(), "key2",
  //           &pinnable_val);
  //   assert(pinnable_val == "value");
  // }

  // {
  //   std::string string_val;
  //   // If it cannot pin the value, it copies the value to its internal
  //   buffer.
  //   // The intenral buffer could be set during construction.
  //   PinnableSlice pinnable_val(&string_val);
  //   db->Get(ReadOptions(Env::IO_SRC_USER), db->DefaultColumnFamily(), "key2",
  //           &pinnable_val);
  //   assert(pinnable_val == "value");
  //   // If the value is not pinned, the internal buffer must have the value.
  //   assert(pinnable_val.IsPinned() || string_val == "value");
  // }

  // // for (int i = 0; i < 1000000; i++) {
  // //   db->Put(WriteOptions(), "key" + std::to_string(i),
  // //           "value" + std::string(100, 'v'));
  // // }

  // // {
  // //   db->Flush(FlushOptions());
  // //   CompactRangeOptions coptions;

  // //   auto start = Slice("key0");
  // //   auto end = Slice("key999999");

  // //   s = db->CompactRange(coptions, &start, &end);
  // //   assert(s.ok());
  // // }

  {
    auto iter = db->NewIterator(ReadOptions(Env::IO_SRC_USER));
    for (iter->Seek("key0"); iter->Valid(); iter->Next()) {
      assert(iter->value().starts_with("v"));
    }
    delete iter;
  }

  delete db;

  TokenLimiter::PrintStatus();
  return 0;
}
