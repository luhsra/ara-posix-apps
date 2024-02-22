#!/usr/bin/env python
"""Build and install the libmicrohttpd."""
import argparse
import sys
import os
import shutil
import subprocess

from pathlib import Path


def eprint(*args):
    """Error print"""
    print(*args, file=sys.stderr)


def run(message, cmd, **kwargs):
    """Print and execute a command."""
    env_fmt = ''
    if 'env' in kwargs:
        env_diff = set(kwargs['env'].items()) - set(os.environ.items())
        env_fmt = ' '.join([f"{key}='{val}'" for key, val in env_diff])
    eprint(message + ':', env_fmt, ' '.join([f"'{x}'" for x in cmd]))
    subprocess.run(cmd, check=True, **kwargs)


def mknew(s_dir):
    if s_dir.is_dir():
        shutil.rmtree(s_dir)
    s_dir.mkdir()


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('--build-dir',
                        help='Directory for the Make build.',
                        required=True,
                        type=Path)
    parser.add_argument('--src-dir',
                        help='Directory for the sources.',
                        required=True,
                        type=Path)
    # parser.add_argument('--musl-install-dir',
    #                     help='Directory for the Musl install.',
    #                     required=True,
    #                     type=Path)
    parser.add_argument('--make-program',
                        help='Make executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--get-bc-program',
                        help='get-bc executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--llvm-objcopy-program',
                        help='llvm-objcopy executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--llvm-ld-program',
                        help='lld executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--gclang-program',
                        help='gclang executable.',
                        required=True,
                        type=Path)
    parser.add_argument('--bc-output',
                        help='Bitcode output file.',
                        required=True,
                        type=Path)
    parser.add_argument('--llvm-bindir',
                        help='Directory that contains the LLVM tools.',
                        required=True,
                        type=Path)
    parser.add_argument('--jobs',
                        help='Run Make with that many jobs.',
                        type=int)
    args = parser.parse_args()

    if args.jobs:
        jobs = args.jobs
    else:
        jobs = len(os.sched_getaffinity(0))

    # the build system is make based and does not support out of tree builds so copy everything into the build dir
    if args.build_dir.is_dir():
        shutil.rmtree(args.build_dir)
    shutil.copytree(args.src_dir, args.build_dir, ignore=lambda *_: ['.git'])

    assert args.src_dir.is_dir()
    assert args.llvm_bindir.is_dir()
    assert args.make_program.is_file()
    assert args.get_bc_program.is_file()
    assert args.llvm_objcopy_program.is_file()
    assert args.llvm_ld_program.is_file()
    assert args.gclang_program.is_file()

    m_env = {**os.environ}
    m_env['LLVM_COMPILER_PATH'] = str(args.llvm_bindir.absolute())
    m_env['GLLVM_OBJCOPY'] = str(args.llvm_objcopy_program.absolute())
    m_env['GLLVM_LD'] = str(args.llvm_ld_program.absolute())
    m_env['CC'] = str(args.gclang_program.absolute())

    run('Executing bootstrap', ['./bootstrap'], cwd=args.build_dir, env=m_env)

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

    run('Executing configure', configure_cmd, cwd=args.build_dir, env=m_env)

    make_cmd = [args.make_program, f'-j{jobs}']
    run('Executing Make', make_cmd, cwd=args.build_dir, env=m_env)

    image = args.build_dir / 'src' / 'microhttpd' / '.libs' / 'libmicrohttpd.a'
    assert image.is_file()

    get_bc_cmd = [
        args.get_bc_program, '-o',
        args.bc_output.absolute(),
        image.absolute()
    ]
    run('Executing get-bc', get_bc_cmd, cwd=args.build_dir, env=m_env)


if __name__ == '__main__':
    main()
