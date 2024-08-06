libmicrohttpd_proj = subproject('libmicrohttpd')
libmicrohttpd_orig_proj = subproject('libmicrohttpd-orig')

libmhd_dir = libmicrohttpd_proj.get_variable('src_dir')
fileserver_example_dirs_c = libmicrohttpd_proj.get_variable('fileserver_example_dirs')
fp_translation_map = libmicrohttpd_proj.get_variable('fp_translation_map')

libmhd_orig_dir = libmicrohttpd_proj.get_variable('src_dir')

llvm_bindir = toolchains.get_variable('llvm_bindir')
llvm_ld = toolchains.get_variable('llvm_ld')
llvm_objcopy = toolchains.get_variable('llvm_objcopy')

# gllvm
gllvm_meson = subproject('gllvm-meson')
get_bc = gllvm_meson.get_variable('get_bc')

build_tools_env = gllvm_meson.get_variable('build_tools_env')

py3_mod = import('python')
py3_inst = py3_mod.find_installation('python3')

make = find_program('make', required: true)
# not directly used, but used as part of the script, therefore check already here
find_program('autoconf', required: true)
find_program('automake', required: true)

# adapted build
libmhd_build = meson.current_build_dir() / 'libmicrohttpd_build'
libmhd_fp_map = libmhd_build / 'function_pointer_translation_map.json'
libmhd_bc = custom_target('libmhd-bc',
  output: 'libmicrohttpd.bc', # output should also be libmhd_fp_map, this is not possible in Meson currently
  env: build_tools_env,
  command: [
    py3_inst, files('make_libmicrohttpd_bitcode.py'),
    '--build-dir', libmhd_build,
    '--src-dir', libmhd_dir,
    '--llvm-bindir', llvm_bindir,
    '--make-program', make.full_path(),
    '--get-bc-program', get_bc.full_path(),
    '--llvm-ld-program', llvm_ld.full_path(),
    '--llvm-objcopy-program', llvm_objcopy.full_path(),
    '--output', '@OUTPUT0@',
    '--gclang-program', musl_clang['bin'],
    # this could be done afterwards and with pure Meson, if fs.copyfile would support that
    # see https://github.com/mesonbuild/meson/issues/12755
    '--translation-map-input', fp_translation_map,
    '--translation-map-output', libmhd_fp_map,
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

libmicrohttpd_app = {
  'name': 'libmicrohttpd',
  'll': fileserver_example_dirs,
  'fp_corrections': [musl_corrections.full_path(), libmhd_fp_map],
}

# original build
libmhd_orig_build = meson.current_build_dir() / 'libmicrohttpd_orig_build'
libmhd_orig_bc = custom_target('libmhd-orig-bc',
  output: 'libmicrohttpd.orig.bc',
  env: build_tools_env,
  command: [
    py3_inst, files('make_libmicrohttpd_bitcode.py'),
    '--build-dir', libmhd_orig_build,
    '--src-dir', libmhd_orig_dir,
    '--llvm-bindir', llvm_bindir,
    '--make-program', make.full_path(),
    '--get-bc-program', get_bc.full_path(),
    '--llvm-ld-program', llvm_ld.full_path(),
    '--llvm-objcopy-program', llvm_objcopy.full_path(),
    '--output', '@OUTPUT0@',
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

warning('TODO: fileserver-example-dirs from libmicrohttpd uses getc etc in musl where syscalls are function pointers.')
libmicrohttpd_orig_app = {
  'name': 'libmicrohttpd-orig',
  'll': fileserver_example_dirs_orig,
  'fp_corrections': [musl_corrections.full_path()],
}
