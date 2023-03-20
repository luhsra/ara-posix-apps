project('ara-posix-apps', 'cpp',
    default_options : ['warning_level=3',
                       'cpp_std=c++17',
                       'buildtype=debugoptimized'])

## llvm dependencies
llvm_version = ['>=14', '<15']
llvm_dep = dependency('llvm', method: 'config-tool', version: llvm_version, include_type: 'system')

llvm_bindir = llvm_dep.get_variable(configtool: 'bindir')
clang = find_program(llvm_bindir / 'clang', version: llvm_version)
llc = find_program(llvm_bindir / 'llc', version: llvm_version)
llvm_dis = find_program(llvm_bindir / 'llvm-dis', version: llvm_version)
llvm_link = find_program(llvm_bindir / 'llvm-link', version: llvm_version)
llvm_opt = find_program(llvm_bindir / 'opt', version: llvm_version)

# wllvm
wllvm = find_program('wllvm', required: true)
extract_bc = find_program('extract-bc', required: true) # provided by wllvm

# tools
make = find_program('make', required: true)
realpath = find_program('realpath', required: true)
autoconf = find_program('autoconf', required: true)
automake = find_program('automake', required: true)
nproc = find_program('nproc', required: true)
cat = find_program('cat', required: true)
nop = find_program('true', required: true)
objcopy = find_program('objcopy', required: true)
awk = find_program('awk', required: true)

## ara-link
ara_link = find_program('ara-link', version: llvm_version, required: false)
if not ara_link.found()
    ara_link_proj = subproject('ara-link')
    ara_link = ara_link_proj.get_variable('ara_link')
    message('Using ara-link from subproject.')
endif

subdir('appl')
