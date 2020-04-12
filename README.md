# unmojibake_zip

Handle zip file with mojibake filenames.

Give a zip file with non-ascii filenames that are not part of current locale, extract and re-zip.

Usage:

  mojibake_zip.py original.zip filename_encoding new.zip

Example usage, extract Japanese zipfile in Western European locale:

  mojibake_zip.py original.zip shiftjis new.zip
