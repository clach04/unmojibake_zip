#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Handle MojiBake zip files.

Very dumb script to:

  * unzip a .zip file to disk- using specified encoding
  * then re-zip up from disk to a new .zip file (hopefully with Unicode encoded filenames to avoid further mojibake)

Almost certainly Python 2 only, as it expects string (byte) encoded filenames.
Only tested under Microsoft Windows (with cp1252 locale) with Shift-JIS Zipfile.
"""

import os
import sys
from zipfile import ZipFile, ZIP_DEFLATED

def unpack(archname, filename_encoding=None):
    arch = ZipFile(archname, 'r')
    for orig_path in arch.namelist():
        path = orig_path 
        print(repr(path))
        if filename_encoding:
            path = path.decode(filename_encoding)
        # NOTE unix style path
        if path.startswith('/') or path.startswith('\\'):  # windows style added just-in-case - maybe overkill, not seen a need for this in the wild
            path = path[1:]
        dname = os.path.dirname(path)
        if dname and not os.path.exists(dname):
            os.makedirs(dname)
        print(repr(path))
        if not path.endswith('/'):
            # this is a file
            data = arch.read(orig_path)
            f = open(path, 'wb')
            f.write(data)
    f.close()
    arch.close()

def pack(archname, paths=None, flist=None):
    if os.path.exists(archname):
        os.unlink(archname)
    if not flist:
        flist = []
        paths = paths or [u'.']
        # TODO force unicode strings for paths
        for path in paths:
            for root, dirs, files in os.walk(path):
                for fname in files:
                    fname = os.path.join(root, fname)
                    flist.append(fname)
    arch = ZipFile(archname, 'w', ZIP_DEFLATED)
    # TODO force unicode strings for flist
    for fname in flist:
        # . is bad for py24 under win,
        # py 2.5 generates more sane entries for:
        #   './filename' and '.\\filename'
        print(repr(fname))
        fname = os.path.normpath(fname)
        arch.write(fname)
    arch.close()


def doit(zip_filename, new_zip_filename, filename_encoding=None,):
    unpack(zip_filename, filename_encoding)
    pack(new_zip_filename, paths=[u'.'])  # Force Unicode string, ergo Unicode filenames


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # no error handling, no helpful error message, deal with it :-p
    zip_filename = argv[1]
    filename_encoding = argv[2]
    new_zip_filename = argv[3]

    doit(zip_filename, new_zip_filename, filename_encoding)

    return 0


if __name__ == "__main__":
    sys.exit(main())
