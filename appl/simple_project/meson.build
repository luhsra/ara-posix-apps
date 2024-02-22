lls = []
foreach source : ['bar.c', 'foo.c']
  tgt = custom_target(fs.name(source),
    input: source,
    output: '@BASENAME@.ll',
    depfile: '@BASENAME@_dep',
    command: clang_c_to_ir_cmd + ['-I', musl_include['include']],
    depends: musl_include['dep']
  )
  lls += [tgt]
endforeach

simple_project = custom_target('simple-project',
  input: [lls, musl_ll],
  output: 'simple-project.ll',
  command: llvm_link_cmd,
)

posix_targets += [simple_project]
