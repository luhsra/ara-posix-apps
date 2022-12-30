
# All non musl libc linked llvm files
foreach appl : appl_list
  posix_target = custom_target('posix_' + appl,
                            output : [appl + '.ll'],
                            # See custom targets in appl/POSIX/meson.build for more information
                            depends : posix_make_cust_target,
                            command : ['true'])
  posix_apps_dict += {appl: posix_target}
endforeach
