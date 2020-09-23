{'targets': [{
    'target_name': 'leveldb'
  , 'variables': {
        'ldbversion': 'rocksdb'
    }
  , 'type': 'static_library'
		# Overcomes an issue with the linker and thin .a files on SmartOS
  , 'standalone_static_library': 1
  , 'dependencies': [
        '../snappy/snappy.gyp:snappy'
    ]
  , 'direct_dependent_settings': {
        'include_dirs': [
            'leveldb-<(ldbversion)/include/'
            # , 'leveldb-<(ldbversion)/port/'
            # , 'leveldb-<(ldbversion)/util'
            # , 'leveldb-<(ldbversion)/'
        ]
    }
  , 'defines': [
        'SNAPPY=1'
    ]
  , 'include_dirs': [
        'leveldb-<(ldbversion)/'
      , 'leveldb-<(ldbversion)/include/'
      , 'leveldb-<(ldbversion)/third-party/folly/'
     ]
  , 'conditions': [
        ['OS == "win"', {
            'include_dirs': [
                 'leveldb-<(ldbversion)/port/win/'
            ]
          , 'defines': [
                'LEVELDB_PLATFORM_UV=1'
              , 'OS_WIN=1'
              , 'NOMINMAX=1'
              , '_HAS_EXCEPTIONS=1'
            ]
          , 'sources': [
               'leveldb-<(ldbversion)/port/win/port_win.cc'
             , 'leveldb-<(ldbversion)/port/win/io_win.cc'
             , 'leveldb-<(ldbversion)/port/win/xpress_win.cc'
             , 'leveldb-<(ldbversion)/port/win/env_default.cc'
             , 'leveldb-<(ldbversion)/port/win/env_win.cc'
             , 'leveldb-<(ldbversion)/port/win/win_logger.cc'
             , 'leveldb-<(ldbversion)/port/win/win_thread.cc'
            ]
          , 'msvs_settings': {
                'VCCLCompilerTool': {
                    'EnableFunctionLevelLinking': 'true'
                  , 'ExceptionHandling': '2'
                  , 'DisableSpecificWarnings': [ '4355', '4530' ,'4267', '4244' ]
                }
            }
          # Must define RuntimeTypeInfo per configuration to override
          # the default setting (see nodejs/node-gyp#857 and #26).
          , 'configurations': {
                'Debug': {
                    'msvs_settings': {
                        'VCCLCompilerTool': {
                            'RuntimeTypeInfo': 'true'
                        }
                    }
                },
                'Release': {
                    'msvs_settings': {
                        'VCCLCompilerTool': {
                            'RuntimeTypeInfo': 'true'
                        }
                    }
                }
            }
        }, { # OS != "win"
            'sources': [
                'leveldb-<(ldbversion)/port/port_posix.cc'
              , 'leveldb-<(ldbversion)/port/port_posix.h'
              , 'leveldb-<(ldbversion)/env/env_posix.cc'
            ]
          , 'defines': [
                'ROCKSDB_PLATFORM_POSIX=1'
            ]
          , 'ccflags': [
                '-fno-builtin-memcmp'
              , '-fPIC'
            ]
          , 'cflags': [ '-std=c++0x' ]
          , 'cflags!': [ '-fno-tree-vrp', '-fno-rtti' ]
          , 'cflags_cc!': [ '-fno-rtti' ]
          # , 'cflags_cc+': [ '-frtti' ]
        }]
      , ['OS != "win"' and 'OS != "freebsd"', {
            'cflags': [
                '-Wno-sign-compare'
              , '-Wno-unused-but-set-variable'
            ]
        }]
      , ['OS == "linux"', {
            'defines': [
                'OS_LINUX=1',
                'ROCKSDB_LIB_IO_POSIX=1'
            ]
          , 'libraries': [
                '-lpthread'
            ]
          , 'ccflags': [
                '-pthread'
                '-fexceptions'
            ]
          , 'cflags!': [ '-fno-exceptions' ]
          , 'cflags_cc!': [ '-fno-exceptions' ]
        }]
      , ['OS == "freebsd"', {
            'defines': [
                'OS_FREEBSD=1'
              , '_REENTRANT=1'
            ]
          , 'libraries': [
                '-lpthread'
            ]
          , 'ccflags': [
                '-pthread'
            ]
          , 'cflags': [
                '-Wno-sign-compare'
            ]
        }]
      , ['OS == "openbsd"', {
            'defines': [
                'OS_OPENBSD=1'
              , '_REENTRANT=1'
            ]
          , 'libraries': [
                '-lpthread'
            ]
          , 'ccflags': [
                '-pthread'
            ]
          , 'cflags': [
                '-Wno-sign-compare'
            ]
        }]
      , ['OS == "solaris"', {
            'defines': [
                'OS_SOLARIS=1'
              , '_REENTRANT=1'
            ]
          , 'libraries': [
                '-lrt'
              , '-lpthread'
            ]
          , 'ccflags': [
                '-pthread'
            ]
        }]
      , ['OS == "mac"', {
            'defines': [
                'OS_MACOSX=1',
                'ROCKSDB_LIB_IO_POSIX=1',
                'ROCKSDB_BACKTRACE=1'
            ]
          , 'libraries': []
          , 'ccflags': []
          , 'xcode_settings': {
                'WARNING_CFLAGS': [
                    '-Wno-sign-compare'
                  , '-Wno-unused-variable'
                  , '-Wno-unused-function'
                ]
                , 'OTHER_CPLUSPLUSFLAGS': [
                    '-mmacosx-version-min=10.8'
                  , '-std=c++11'
                  , '-stdlib=libc++'
                  , '-march=native'
                  , '-fno-omit-frame-pointer'
                  , '-momit-leaf-frame-pointer'
                ]
# , 'OTHER_LDFLAGS': ['-stdlib=libc++']
                , 'GCC_ENABLE_CPP_RTTI': 'YES'
                , 'GCC_ENABLE_CPP_EXCEPTIONS': 'YES'
                , 'MACOSX_DEPLOYMENT_TARGET': '10.8'
            }
        }]
    ]
  , 'sources': [
      'leveldb-<(ldbversion)/util/build_version.cc'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/detail/Futex.cpp'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/detail/Futex.h'  
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/AtomicNotification.cpp'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/AtomicNotification.h'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/DistributedMutex.cpp'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/DistributedMutex.h'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/ParkingLot.cpp'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/ParkingLot.h'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/WaitOptions.cpp'
      , 'leveldb-<(ldbversion)/third-party/folly/folly/synchronization/WaitOptions.h'      
      , 'leveldb-<(ldbversion)/cache/cache.cc'
      , 'leveldb-<(ldbversion)/cache/clock_cache.cc'
      , 'leveldb-<(ldbversion)/cache/lru_cache.cc'
      , 'leveldb-<(ldbversion)/cache/sharded_cache.cc'
      , 'leveldb-<(ldbversion)/db/arena_wrapped_db_iter.cc'
      , 'leveldb-<(ldbversion)/db/blob/blob_file_addition.cc'
      , 'leveldb-<(ldbversion)/db/blob/blob_file_builder.cc'
      , 'leveldb-<(ldbversion)/db/blob/blob_file_garbage.cc'
      , 'leveldb-<(ldbversion)/db/blob/blob_file_meta.cc'
      , 'leveldb-<(ldbversion)/db/blob/blob_log_format.cc'
      , 'leveldb-<(ldbversion)/db/blob/blob_log_reader.cc'
      , 'leveldb-<(ldbversion)/db/blob/blob_log_writer.cc'
      , 'leveldb-<(ldbversion)/db/builder.cc'
      , 'leveldb-<(ldbversion)/db/c.cc'
      , 'leveldb-<(ldbversion)/db/column_family.cc'
      , 'leveldb-<(ldbversion)/db/compacted_db_impl.cc'
      , 'leveldb-<(ldbversion)/db/compaction/compaction.cc'
      , 'leveldb-<(ldbversion)/db/compaction/compaction_iterator.cc'
      , 'leveldb-<(ldbversion)/db/compaction/compaction_job.cc'
      , 'leveldb-<(ldbversion)/db/compaction/compaction_picker.cc'
      , 'leveldb-<(ldbversion)/db/compaction/compaction_picker_fifo.cc'
      , 'leveldb-<(ldbversion)/db/compaction/compaction_picker_level.cc'
      , 'leveldb-<(ldbversion)/db/compaction/compaction_picker_universal.cc'
      , 'leveldb-<(ldbversion)/db/compaction/sst_partitioner.cc'
      , 'leveldb-<(ldbversion)/db/convenience.cc'
      , 'leveldb-<(ldbversion)/db/db_filesnapshot.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_compaction_flush.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_debug.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_experimental.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_files.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_open.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_readonly.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_secondary.cc'
      , 'leveldb-<(ldbversion)/db/db_impl/db_impl_write.cc'
      , 'leveldb-<(ldbversion)/db/db_info_dumper.cc'
      , 'leveldb-<(ldbversion)/db/db_iter.cc'
      , 'leveldb-<(ldbversion)/db/dbformat.cc'
      , 'leveldb-<(ldbversion)/db/error_handler.cc'
      , 'leveldb-<(ldbversion)/db/event_helpers.cc'
      , 'leveldb-<(ldbversion)/db/experimental.cc'
      , 'leveldb-<(ldbversion)/db/external_sst_file_ingestion_job.cc'
      , 'leveldb-<(ldbversion)/db/file_indexer.cc'
      , 'leveldb-<(ldbversion)/db/flush_job.cc'
      , 'leveldb-<(ldbversion)/db/flush_scheduler.cc'
      , 'leveldb-<(ldbversion)/db/forward_iterator.cc'
      , 'leveldb-<(ldbversion)/db/import_column_family_job.cc'
      , 'leveldb-<(ldbversion)/db/internal_stats.cc'
      , 'leveldb-<(ldbversion)/db/logs_with_prep_tracker.cc'
      , 'leveldb-<(ldbversion)/db/log_reader.cc'
      , 'leveldb-<(ldbversion)/db/log_writer.cc'
      , 'leveldb-<(ldbversion)/db/malloc_stats.cc'
      , 'leveldb-<(ldbversion)/db/memtable.cc'
      , 'leveldb-<(ldbversion)/db/memtable_list.cc'
      , 'leveldb-<(ldbversion)/db/merge_helper.cc'
      , 'leveldb-<(ldbversion)/db/merge_operator.cc'
      , 'leveldb-<(ldbversion)/db/range_del_aggregator.cc'
      , 'leveldb-<(ldbversion)/db/range_tombstone_fragmenter.cc'
      , 'leveldb-<(ldbversion)/db/repair.cc'
      , 'leveldb-<(ldbversion)/db/snapshot_impl.cc'
      , 'leveldb-<(ldbversion)/db/table_cache.cc'
      , 'leveldb-<(ldbversion)/db/table_properties_collector.cc'
      , 'leveldb-<(ldbversion)/db/transaction_log_impl.cc'
      , 'leveldb-<(ldbversion)/db/trim_history_scheduler.cc'
      , 'leveldb-<(ldbversion)/db/version_builder.cc'
      , 'leveldb-<(ldbversion)/db/version_edit.cc'
      , 'leveldb-<(ldbversion)/db/version_edit_handler.cc'
      , 'leveldb-<(ldbversion)/db/version_set.cc'
      , 'leveldb-<(ldbversion)/db/wal_edit.cc'
      , 'leveldb-<(ldbversion)/db/wal_manager.cc'
      , 'leveldb-<(ldbversion)/db/write_batch.cc'
      , 'leveldb-<(ldbversion)/db/write_batch_base.cc'
      , 'leveldb-<(ldbversion)/db/write_controller.cc'
      , 'leveldb-<(ldbversion)/db/write_thread.cc'
      , 'leveldb-<(ldbversion)/env/env.cc'
      , 'leveldb-<(ldbversion)/env/env_chroot.cc'
      , 'leveldb-<(ldbversion)/env/env_encryption.cc'
      , 'leveldb-<(ldbversion)/env/env_hdfs.cc'
      , 'leveldb-<(ldbversion)/env/env_posix.cc'
      , 'leveldb-<(ldbversion)/env/file_system.cc'
      , 'leveldb-<(ldbversion)/env/fs_posix.cc'
      , 'leveldb-<(ldbversion)/env/file_system_tracer.cc'
      , 'leveldb-<(ldbversion)/env/io_posix.cc'
      , 'leveldb-<(ldbversion)/env/mock_env.cc'
      , 'leveldb-<(ldbversion)/file/delete_scheduler.cc'
      , 'leveldb-<(ldbversion)/file/file_prefetch_buffer.cc'
      , 'leveldb-<(ldbversion)/file/file_util.cc'
      , 'leveldb-<(ldbversion)/file/filename.cc'
      , 'leveldb-<(ldbversion)/file/random_access_file_reader.cc'
      , 'leveldb-<(ldbversion)/file/read_write_util.cc'
      , 'leveldb-<(ldbversion)/file/readahead_raf.cc'
      , 'leveldb-<(ldbversion)/file/sequence_file_reader.cc'
      , 'leveldb-<(ldbversion)/file/sst_file_manager_impl.cc'
      , 'leveldb-<(ldbversion)/file/writable_file_writer.cc'
      , 'leveldb-<(ldbversion)/logging/auto_roll_logger.cc'
      , 'leveldb-<(ldbversion)/logging/event_logger.cc'
      , 'leveldb-<(ldbversion)/logging/log_buffer.cc'
      , 'leveldb-<(ldbversion)/memory/arena.cc'
      , 'leveldb-<(ldbversion)/memory/concurrent_arena.cc'
      , 'leveldb-<(ldbversion)/memory/jemalloc_nodump_allocator.cc'
      , 'leveldb-<(ldbversion)/memory/memkind_kmem_allocator.cc'
      , 'leveldb-<(ldbversion)/memtable/alloc_tracker.cc'
      , 'leveldb-<(ldbversion)/memtable/hash_linklist_rep.cc'
      , 'leveldb-<(ldbversion)/memtable/hash_skiplist_rep.cc'
      , 'leveldb-<(ldbversion)/memtable/skiplistrep.cc'
      , 'leveldb-<(ldbversion)/memtable/vectorrep.cc'
      , 'leveldb-<(ldbversion)/memtable/write_buffer_manager.cc'
      , 'leveldb-<(ldbversion)/monitoring/histogram.cc'
      , 'leveldb-<(ldbversion)/monitoring/histogram_windowing.cc'
      , 'leveldb-<(ldbversion)/monitoring/in_memory_stats_history.cc'
      , 'leveldb-<(ldbversion)/monitoring/instrumented_mutex.cc'
      , 'leveldb-<(ldbversion)/monitoring/iostats_context.cc'
      , 'leveldb-<(ldbversion)/monitoring/perf_context.cc'
      , 'leveldb-<(ldbversion)/monitoring/perf_level.cc'
      , 'leveldb-<(ldbversion)/monitoring/persistent_stats_history.cc'
      , 'leveldb-<(ldbversion)/monitoring/statistics.cc'
      , 'leveldb-<(ldbversion)/monitoring/stats_dump_scheduler.cc'
      , 'leveldb-<(ldbversion)/monitoring/thread_status_impl.cc'
      , 'leveldb-<(ldbversion)/monitoring/thread_status_updater.cc'
      , 'leveldb-<(ldbversion)/monitoring/thread_status_updater_debug.cc'
      , 'leveldb-<(ldbversion)/monitoring/thread_status_util.cc'
      , 'leveldb-<(ldbversion)/monitoring/thread_status_util_debug.cc'
      , 'leveldb-<(ldbversion)/options/cf_options.cc'
      , 'leveldb-<(ldbversion)/options/configurable.cc'
      , 'leveldb-<(ldbversion)/options/db_options.cc'
      , 'leveldb-<(ldbversion)/options/options.cc'
      , 'leveldb-<(ldbversion)/options/options_helper.cc'
      , 'leveldb-<(ldbversion)/options/options_parser.cc'
      , 'leveldb-<(ldbversion)/port/port_posix.cc'
      , 'leveldb-<(ldbversion)/port/stack_trace.cc'
      , 'leveldb-<(ldbversion)/table/adaptive/adaptive_table_factory.cc'
      , 'leveldb-<(ldbversion)/table/block_based/binary_search_index_reader.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_based_filter_block.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_based_table_builder.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_based_table_factory.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_based_table_iterator.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_based_table_reader.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_builder.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_prefetcher.cc'
      , 'leveldb-<(ldbversion)/table/block_based/block_prefix_index.cc'
      , 'leveldb-<(ldbversion)/table/block_based/data_block_hash_index.cc'
      , 'leveldb-<(ldbversion)/table/block_based/data_block_footer.cc'
      , 'leveldb-<(ldbversion)/table/block_based/filter_block_reader_common.cc'
      , 'leveldb-<(ldbversion)/table/block_based/filter_policy.cc'
      , 'leveldb-<(ldbversion)/table/block_based/flush_block_policy.cc'
      , 'leveldb-<(ldbversion)/table/block_based/full_filter_block.cc'
      , 'leveldb-<(ldbversion)/table/block_based/hash_index_reader.cc'
      , 'leveldb-<(ldbversion)/table/block_based/index_builder.cc'
      , 'leveldb-<(ldbversion)/table/block_based/index_reader_common.cc'
      , 'leveldb-<(ldbversion)/table/block_based/parsed_full_filter_block.cc'
      , 'leveldb-<(ldbversion)/table/block_based/partitioned_filter_block.cc'
      , 'leveldb-<(ldbversion)/table/block_based/partitioned_index_iterator.cc'
      , 'leveldb-<(ldbversion)/table/block_based/partitioned_index_reader.cc'
      , 'leveldb-<(ldbversion)/table/block_based/reader_common.cc'
      , 'leveldb-<(ldbversion)/table/block_based/uncompression_dict_reader.cc'
      , 'leveldb-<(ldbversion)/table/block_fetcher.cc'
      , 'leveldb-<(ldbversion)/table/cuckoo/cuckoo_table_builder.cc'
      , 'leveldb-<(ldbversion)/table/cuckoo/cuckoo_table_factory.cc'
      , 'leveldb-<(ldbversion)/table/cuckoo/cuckoo_table_reader.cc'
      , 'leveldb-<(ldbversion)/table/format.cc'
      , 'leveldb-<(ldbversion)/table/get_context.cc'
      , 'leveldb-<(ldbversion)/table/iterator.cc'
      , 'leveldb-<(ldbversion)/table/merging_iterator.cc'
      , 'leveldb-<(ldbversion)/table/meta_blocks.cc'
      , 'leveldb-<(ldbversion)/table/persistent_cache_helper.cc'
      , 'leveldb-<(ldbversion)/table/plain/plain_table_bloom.cc'
      , 'leveldb-<(ldbversion)/table/plain/plain_table_builder.cc'
      , 'leveldb-<(ldbversion)/table/plain/plain_table_factory.cc'
      , 'leveldb-<(ldbversion)/table/plain/plain_table_index.cc'
      , 'leveldb-<(ldbversion)/table/plain/plain_table_key_coding.cc'
      , 'leveldb-<(ldbversion)/table/plain/plain_table_reader.cc'
      , 'leveldb-<(ldbversion)/table/sst_file_dumper.cc'
      , 'leveldb-<(ldbversion)/table/sst_file_reader.cc'
      , 'leveldb-<(ldbversion)/table/sst_file_writer.cc'
      , 'leveldb-<(ldbversion)/table/table_factory.cc'
      , 'leveldb-<(ldbversion)/table/table_properties.cc'
      , 'leveldb-<(ldbversion)/table/two_level_iterator.cc'
      , 'leveldb-<(ldbversion)/test_util/sync_point.cc'
      , 'leveldb-<(ldbversion)/test_util/sync_point_impl.cc'
      , 'leveldb-<(ldbversion)/test_util/transaction_test_util.cc'
      , 'leveldb-<(ldbversion)/tools/dump/db_dump_tool.cc'
      , 'leveldb-<(ldbversion)/trace_replay/trace_replay.cc'
      , 'leveldb-<(ldbversion)/trace_replay/block_cache_tracer.cc'
      , 'leveldb-<(ldbversion)/trace_replay/io_tracer.cc'
      , 'leveldb-<(ldbversion)/util/build_version.cc'
      , 'leveldb-<(ldbversion)/util/coding.cc'
      , 'leveldb-<(ldbversion)/util/compaction_job_stats_impl.cc'
      , 'leveldb-<(ldbversion)/util/comparator.cc'
      , 'leveldb-<(ldbversion)/util/compression_context_cache.cc'
      , 'leveldb-<(ldbversion)/util/concurrent_task_limiter_impl.cc'
      , 'leveldb-<(ldbversion)/util/crc32c.cc'
      , 'leveldb-<(ldbversion)/util/dynamic_bloom.cc'
      , 'leveldb-<(ldbversion)/util/hash.cc'
      , 'leveldb-<(ldbversion)/util/murmurhash.cc'
      , 'leveldb-<(ldbversion)/util/random.cc'
      , 'leveldb-<(ldbversion)/util/rate_limiter.cc'
      , 'leveldb-<(ldbversion)/util/slice.cc'
      , 'leveldb-<(ldbversion)/util/file_checksum_helper.cc'
      , 'leveldb-<(ldbversion)/util/status.cc'
      , 'leveldb-<(ldbversion)/util/string_util.cc'
      , 'leveldb-<(ldbversion)/util/thread_local.cc'
      , 'leveldb-<(ldbversion)/util/threadpool_imp.cc'
      , 'leveldb-<(ldbversion)/util/xxhash.cc'
      , 'leveldb-<(ldbversion)/utilities/backupable/backupable_db.cc'
      , 'leveldb-<(ldbversion)/utilities/blob_db/blob_compaction_filter.cc'
      , 'leveldb-<(ldbversion)/utilities/blob_db/blob_db.cc'
      , 'leveldb-<(ldbversion)/utilities/blob_db/blob_db_impl.cc'
      , 'leveldb-<(ldbversion)/utilities/blob_db/blob_db_impl_filesnapshot.cc'
      , 'leveldb-<(ldbversion)/utilities/blob_db/blob_file.cc'
      , 'leveldb-<(ldbversion)/utilities/cassandra/cassandra_compaction_filter.cc'
      , 'leveldb-<(ldbversion)/utilities/cassandra/format2.cc'
      , 'leveldb-<(ldbversion)/utilities/cassandra/merge_operator2.cc'
      , 'leveldb-<(ldbversion)/utilities/checkpoint/checkpoint_impl.cc'
      , 'leveldb-<(ldbversion)/utilities/compaction_filters/remove_emptyvalue_compactionfilter.cc'
      , 'leveldb-<(ldbversion)/utilities/convenience/info_log_finder.cc'
      , 'leveldb-<(ldbversion)/utilities/debug.cc'
      , 'leveldb-<(ldbversion)/utilities/env_mirror.cc'
      , 'leveldb-<(ldbversion)/utilities/env_timed.cc'
      , 'leveldb-<(ldbversion)/utilities/fault_injection_env.cc'
      , 'leveldb-<(ldbversion)/utilities/fault_injection_fs.cc'
      , 'leveldb-<(ldbversion)/utilities/leveldb_options/leveldb_options.cc'
      , 'leveldb-<(ldbversion)/utilities/memory/memory_util.cc'
      , 'leveldb-<(ldbversion)/utilities/merge_operators/max.cc'
      , 'leveldb-<(ldbversion)/utilities/merge_operators/put.cc'
      , 'leveldb-<(ldbversion)/utilities/merge_operators/sortlist.cc'
      , 'leveldb-<(ldbversion)/utilities/merge_operators/string_append/stringappend.cc'
      , 'leveldb-<(ldbversion)/utilities/merge_operators/string_append/stringappend2.cc'
      , 'leveldb-<(ldbversion)/utilities/merge_operators/uint64add.cc'
      , 'leveldb-<(ldbversion)/utilities/merge_operators/bytesxor.cc'
      , 'leveldb-<(ldbversion)/utilities/object_registry.cc'
      , 'leveldb-<(ldbversion)/utilities/option_change_migration/option_change_migration.cc'
      , 'leveldb-<(ldbversion)/utilities/options/options_util.cc'
      , 'leveldb-<(ldbversion)/utilities/persistent_cache/block_cache_tier.cc'
      , 'leveldb-<(ldbversion)/utilities/persistent_cache/block_cache_tier_file.cc'
      , 'leveldb-<(ldbversion)/utilities/persistent_cache/block_cache_tier_metadata.cc'
      , 'leveldb-<(ldbversion)/utilities/persistent_cache/persistent_cache_tier.cc'
      , 'leveldb-<(ldbversion)/utilities/persistent_cache/volatile_tier_impl.cc'
      , 'leveldb-<(ldbversion)/utilities/simulator_cache/cache_simulator.cc'
      , 'leveldb-<(ldbversion)/utilities/simulator_cache/sim_cache.cc'
      , 'leveldb-<(ldbversion)/utilities/table_properties_collectors/compact_on_deletion_collector.cc'
      , 'leveldb-<(ldbversion)/utilities/trace/file_trace_reader_writer.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/lock/lock_tracker.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/lock/point_lock_tracker.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/optimistic_transaction.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/optimistic_transaction_db_impl.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/pessimistic_transaction.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/pessimistic_transaction_db.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/snapshot_checker.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/transaction_base.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/transaction_db_mutex_impl.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/transaction_lock_mgr.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/transaction_util.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/write_prepared_txn.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/write_prepared_txn_db.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/write_unprepared_txn.cc'
      , 'leveldb-<(ldbversion)/utilities/transactions/write_unprepared_txn_db.cc'
      , 'leveldb-<(ldbversion)/utilities/ttl/db_ttl_impl.cc'
      , 'leveldb-<(ldbversion)/utilities/write_batch_with_index/write_batch_with_index.cc'
      , 'leveldb-<(ldbversion)/utilities/write_batch_with_index/write_batch_with_index_internal.cc'
    ]
}]}
