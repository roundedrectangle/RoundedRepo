#!/usr/bin/python3

from pathlib import Path
import argparse
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(#'TweakBuilder',
        description="Build tweaks for PureKFD",
        epilog="Check out the GitHub page for more information."
    )
    parser.add_argument('source', help="Sources of your tweak")
    parser.add_argument('bundleid', help="Your tweak's bundle ID")
    parser.add_argument('-b', '--build', help="The directory to put build artefacts to. The default is <source>/../build. When the directory already exists, it gets cleared")
    parser.add_argument('-d', '--dest', help="The built tweak destenation. The default is <source>/../main.purekfd. When the file already exists, it will be overriden.")
    parser.add_argument('-r', '--keep-build', help="Keep the build directory after building the tweak", action='store_true')
    args = parser.parse_args()

    def ensure_exists(path, name):
        path = Path(path)
        if not path.exists():
            parser.error(f"{name} does not exist at: {path}")
        return path

    src = ensure_exists(args.source, 'source')

    build = Path(args.build) if args.build else src.parent / 'build'
    dest = Path(args.dest) if args.dest else src.parent / 'main.purekfd'#f'{args.bundleid}.purekfd'

    shutil.rmtree(build, ignore_errors=True)
    build.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, build / args.bundleid)

    dest.unlink(True)
    archived_dest = Path(shutil.make_archive(dest, 'zip', build))
    archived_dest.rename(dest)

    if not args.keep_build:
        shutil.rmtree(build)

    print("All done! Built tweak is now located at", dest.absolute())