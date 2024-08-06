posix_sources = [
  # {'name': 'filestream_read', 'with_musl': true},  <- TODO, fread in musl leads to a function pointer to different syscalls, see musl/src/stdio/__toread.c
  # {'name': 'filestream_write', 'with_musl': true},  <- TODO, fwrite is like fread, see musl/src/stdio/fwrite.c
  {'name': 'funcpointer_issue', 'with_musl': true},
  {'name': 'ospert_2022_example', 'with_musl': true},
  {'name': 'pipe2_test', 'with_musl': true},
  {'name': 'valueanalyzer_case_1', 'with_musl': true},
  {'name': 'valueanalyzer_case_2', 'with_musl': true},
  {'name': 'valueanalyzer_case_3', 'with_musl': true},
  {'name': 'test_appl' / 'condition_var_broadcast', 'with_musl': true},
  {'name': 'test_appl' / 'condition_variable', 'with_musl': true},
  {'name': 'test_appl' / 'condition_var_initializer', 'with_musl': true},
  {'name': 'test_appl' / 'create_everything', 'with_musl': true},
  {'name': 'test_appl' / 'file_read', 'with_musl': true},
  {'name': 'test_appl' / 'file_readv', 'with_musl': true},
  {'name': 'test_appl' / 'filestream_open', 'with_musl': true},
  {'name': 'test_appl' / 'file_write', 'with_musl': true},
  {'name': 'test_appl' / 'file_writev', 'with_musl': true},
  {'name': 'test_appl' / 'ignore_signal', 'with_musl': true},
  {'name': 'test_appl' / 'instance_graph_stats', 'with_musl': true},
  {'name': 'test_appl' / 'multiple_sigactions', 'with_musl': true},
  {'name': 'test_appl' / 'mutex', 'with_musl': true},
  {'name': 'test_appl' / 'mutex_counter', 'with_musl': true},
  {'name': 'test_appl' / 'mutex_initializer', 'with_musl': true},
  {'name': 'test_appl' / 'nanosleep', 'with_musl': true},
  {'name': 'test_appl' / 'open_twice', 'with_musl': true},
  {'name': 'test_appl' / 'open_two_files', 'with_musl': true},
  {'name': 'test_appl' / 'pipe', 'with_musl': true},
  {'name': 'test_appl' / 'pthread_cancel', 'with_musl': true},
  {'name': 'test_appl' / 'pthread_create', 'with_musl': true},
  {'name': 'test_appl' / 'pthread_detach', 'with_musl': true},
  {'name': 'test_appl' / 'pthread_setname_np', 'with_musl': true},
  {'name': 'test_appl' / 'semaphore', 'with_musl': true},
  {'name': 'test_appl' / 'semaphore_ring_buffer', 'with_musl': true},
  {'name': 'test_appl' / 'set_thread_attr', 'with_musl': true},
  {'name': 'test_appl' / 'sigaction_macro_test', 'with_musl': true},
  {'name': 'test_appl' / 'signal_handler', 'with_musl': true},
  {'name': 'test_appl' / 'signal_handler_siginfo', 'with_musl': true},
  {'name': 'test_appl' / 'sleep', 'with_musl': true},
  {'name': 'test_appl' / 'system_profile_inheritance', 'with_musl': true},
  {'name': 'test_appl' / 'thread_attr_cond_calls', 'with_musl': true},
  {'name': 'test_appl' / 'thread_attr_double_call', 'with_musl': true},
  {'name': 'test_appl' / 'thread_attr_inheritance', 'with_musl': true},
  {'name': 'test_appl' / 'thread_attr_not_unique', 'with_musl': true},
  {'name': 'test_appl' / 'thread_setname_cond_calls', 'with_musl': true},
  {'name': 'test_appl' / 'wrong_call_in_sighandler', 'with_musl': true},
  {'name': 'test_appl' / 'wrong_file_access', 'with_musl': true},
  {'name': 'test_appl' / 'wrong_pipe_access', 'with_musl': true},
  {'name': 'test_appl' / 'no_musl_linkage' / 'clang_global_var_dynamic', 'with_musl': false},
  {'name': 'test_appl' / 'no_musl_linkage' / 'clang_global_var_static', 'with_musl': false},
  {'name': 'test_appl' / 'no_musl_linkage' / 'linux_syscalls', 'with_musl': false},
]

foreach app : posix_sources
  app_name = app['name'].underscorify()
  tgt = custom_target(app_name + '-raw',
    input: files(app['name'] + '.c'),
    output: app_name + '.muslless.ll',
    depfile: app_name + '_dep',
    command: clang_c_to_ir_cmd + ['-nostdinc', '-D_POSIX_C_SOURCE=200809L', '-I', musl_include['include']],
    depends: musl_include['dep'],
  )
  with_musl = tgt
  if app['with_musl']
    with_musl = custom_target(app_name + '-with-musl',
      input: [tgt, musl_ll],
      output: app_name + '.ll',
      command: llvm_link_cmd,
    )
  endif
  posix_apps += [{'name': app_name, 'll': with_musl}]
  set_variable(app_name + '_ll', with_musl)
endforeach

subdir('simple_project')
