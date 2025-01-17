#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2011-2022 Blender Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

__all__ = (
    "main",
)

import os
import shutil
import subprocess
import sys

# todo:
# strip executables


def main() -> int:
    # get parameters
    if len(sys.argv) < 5:
        sys.stderr.write('Excepted arguments: ./build_archive.py name extension install_dir output_dir')
        return 1

    package_name = sys.argv[1]
    extension = sys.argv[2]
    install_dir = sys.argv[3]
    output_dir = sys.argv[4]

    package_archive = os.path.join(output_dir, package_name + '.' + extension)
    package_dir = package_name

    # remove existing package with the same name
    try:
        if os.path.exists(package_archive):
            os.remove(package_archive)
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
    except Exception as ex:
        sys.stderr.write('Failed to clean up old package files: ' + str(ex) + '\n')
        return 1

    # create temporary package dir
    try:
        shutil.copytree(install_dir, package_dir)

        for f in os.listdir(package_dir):
            if f.startswith('makes'):
                os.remove(os.path.join(package_dir, f))
    except Exception as ex:
        sys.stderr.write('Failed to copy install directory: ' + str(ex) + '\n')
        return 1

    # create archive
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        archive_env = os.environ.copy()

        if extension == 'zip':
            archive_cmd = ['zip', '-9', '-r', package_archive, package_dir]
        elif extension == 'tar.xz':
            archive_cmd = ['tar', '-cf', package_archive, '--owner=0', '--group=0',
                           '--use-compress-program=xz', package_dir]
            archive_env['XZ_OPT'] = '-9'
        else:
            sys.stderr.write('Unknown archive extension: ' + extension)
            return 1

        subprocess.check_call(archive_cmd, env=archive_env)
    except Exception as ex:
        sys.stderr.write('Failed to create package archive: ' + str(ex) + '\n')
        return 1

    # empty temporary package dir
    try:
        shutil.rmtree(package_dir)
    except Exception as ex:
        sys.stderr.write('Failed to clean up package directory: ' + str(ex) + '\n')
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
