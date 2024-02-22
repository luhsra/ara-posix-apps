libmicrohttpd_proj = subproject('libmicrohttpd')
libmicrohttpd_orig_proj = subproject('libmicrohttpd-orig')

libmhd_dir = libmicrohttpd_proj.get_variable('src_dir')
fileserver_example_dirs_c = libmicrohttpd_proj.get_variable('fileserver_example_dirs')

libmhd_orig_dir = libmicrohttpd_proj.get_variable('src_dir')

llvm_bindir = toolchains.get_variable('llvm_bindir')
llvm_ld = toolchains.get_variable('llvm_ld')
llvm_objcopy = toolchains.get_variable('llvm_objcopy')

# gllvm
gllvm_meson = subproject('gllvm-meson')
get_bc = gllvm_meson.get_variable('get_bc')

py3_mod = import('python')
py3_inst = py3_mod.find_installation('python3')

make = find_program('make', required: true)
# not directly used, but used as part of the script, therefore check already here
find_program('autoconf', required: true)
find_program('automake', required: true)

# adapted build
libmhd_build = meson.current_build_dir() / 'libmicrohttpd_build'
libmhd_bc = custom_target('libmhd-bc',
  output: 'libmicrohttpd.bc',
  command: [
    py3_inst, files('make_libmicrohttpd_bitcode.py'),
    '--build-dir', libmhd_build,
    '--src-dir', libmhd_dir,
    '--llvm-bindir', llvm_bindir,
    '--make-program', make.full_path(),
    '--get-bc-program', get_bc.full_path(),
    '--llvm-ld-program', llvm_ld.full_path(),
    '--llvm-objcopy-program', llvm_objcopy.full_path(),
    '--bc-output', '@OUTPUT0@',
    '--gclang-program', musl_clang['bin'],
  ],
  depends: musl_clang['dep']
)
libmhd = {'ll': libmhd_bc, 'include': ['-I', libmhd_dir / 'src' / 'include', '-I', libmhd_build]}

fileserver_example_dirs_raw = custom_target('fileserver-example-dirs-raw',
  output: 'fileserver-example-dirs.unlinked.ll',
  input: fileserver_example_dirs_c,
  depfile: 'fileserver-example-dirs.dep',
  command: clang_c_to_ir_cmd + libmhd['include'],
  depends: libmhd['ll'],
)
fileserver_example_dirs = custom_target('fileserver-example-dirs',
  output: 'fileserver-example-dirs.ll',
  input: [fileserver_example_dirs_raw, libmhd['ll'], musl_ll],
  command: llvm_link_cmd,
)
posix_apps += [{'name': 'libmicrohttpd', 'll': fileserver_example_dirs}]

# original build
libmhd_orig_build = meson.current_build_dir() / 'libmicrohttpd_orig_build'
libmhd_orig_bc = custom_target('libmhd-orig-bc',
  output: 'libmicrohttpd.orig.bc',
  command: [
    py3_inst, files('make_libmicrohttpd_bitcode.py'),
    '--build-dir', libmhd_orig_build,
    '--src-dir', libmhd_orig_dir,
    '--llvm-bindir', llvm_bindir,
    '--make-program', make.full_path(),
    '--get-bc-program', get_bc.full_path(),
    '--llvm-ld-program', llvm_ld.full_path(),
    '--llvm-objcopy-program', llvm_objcopy.full_path(),
    '--bc-output', '@OUTPUT0@',
    '--gclang-program', musl_clang['bin'],
  ],
  depends: musl_clang['dep']
)
libmhd_orig = {'ll': libmhd_orig_bc, 'include': ['-I', libmhd_orig_dir / 'src' / 'include', '-I', libmhd_orig_build]}

fileserver_example_dirs_orig_raw = custom_target('fileserver-example-dirs-orig-raw',
  output: 'fileserver-example-dirs.orig.unlinked.ll',
  input: fileserver_example_dirs_c,
  depfile: 'fileserver-example-dirs.dep',
  command: clang_c_to_ir_cmd + libmhd_orig['include'],
  depends: libmhd_orig['ll'],
)
fileserver_example_dirs_orig = custom_target('fileserver-example-dirs-orig',
  output: 'fileserver-example-dirs.orig.ll',
  input: [fileserver_example_dirs_orig_raw, libmhd_orig['ll'], musl_ll],
  command: llvm_link_cmd,
)
posix_apps += [{'name': 'libmicrohttpd-orig', 'll': fileserver_example_dirs_orig}]
