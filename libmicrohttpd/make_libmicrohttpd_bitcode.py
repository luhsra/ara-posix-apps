#!/usr/bin/env python
"""Build libmicrohttpd."""
from shutil import copyfile

from build_tools import run, Builder


class LibMHDBuilder(Builder):
    """Build bitcode for libmicrohttpd."""
    def __init__(self):
        super().__init__(with_make=True, with_gclang=True)

    def _add_other_args(self, parser):
        """Pure workaournd for Meson not able to copy in subdirs."""
        parser.add_argument('--translation-map-input',
                            help="Path to translation map.")
        parser.add_argument('--translation-map-output',
                            help="Path where translation map should be copied.")

    def do_build(self):
        self._copy_src()

        env = self._get_gllvm_env()
        env['CC'] = str(self.args.gclang_program.absolute())

        run('Executing bootstrap', ['./bootstrap'], cwd=self.args.build_dir, env=env)

        configure_cmd = [
            './configure',
            '--disable-nls',
            '--enable-https=no',
            '--without-gnutls',
            '--with-threads=posix',
            '--disable-curl',
            '--disable-largefile',
            '--disable-messages',
            '--disable-dauth',
            '--disable-httpupgrade',
            '--disable-epoll',
            '--disable-poll',
            '--enable-itc=pipe',
            '--disable-postprocessor',
        ]

        run('Executing configure', configure_cmd, cwd=self.args.build_dir, env=env)

        make_cmd = [self.args.make_program, f'-j{self.jobs}']
        run('Executing Make', make_cmd, cwd=self.args.build_dir, env=env)

        image = self.args.build_dir / 'src' / 'microhttpd' / '.libs' / 'libmicrohttpd.a'
        assert image.is_file()

        self._get_bc(image, env)

        if self.args.translation_map_input:
            copyfile(self.args.translation_map_input, self.args.translation_map_output)


if __name__ == '__main__':
    builder = LibMHDBuilder()
    builder.do_build()
