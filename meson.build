project('ara-posix-apps', 'cpp',
    default_options : ['warning_level=3',
                       'cpp_std=c++17',
                       'buildtype=debugoptimized'])

fs = import('fs')

## llvm dependencies
llvm_version = ['>=14', '<15']
llvm_dep = dependency('llvm', method: 'config-tool', version: llvm_version, include_type: 'system')

toolchains = subproject('toolchains')
clang_c_to_ir_cmd = toolchains.get_variable('clang_c_to_ir_cmd')
llvm_link_cmd = toolchains.get_variable('llvm_link_cmd')

nop = find_program('true', required: true)

## musl
musl = subproject('musl-libc')
# musl_dir = musl.get_variable('musl_dir')
musl_include = musl.get_variable('musl_include')
musl_ll = musl.get_variable('musl_ll')
musl_clang = musl.get_variable('musl_clang')
musl_corrections = musl.get_variable('fp_corrections')

# fill apps
posix_apps = []
subdir('appl')

if get_option('build_libmicrohttpd')
  subdir('libmicrohttpd')
endif

posix_apps_tgt = 'posix-apps'
posix_targets = []
foreach app : posix_apps
  posix_targets += [app['ll']]
endforeach
run_target(posix_apps_tgt,
  command: nop,
  depends: posix_targets,
)
summary('Build all POSIX apps', 'meson compile ' + posix_apps_tgt)
