# unmojibake_zip

Handle zip file with mojibake filenames.

Give a zip file with non-ascii filenames that are not part of current locale, extract and re-zip.

Usage, in a temporary and empty directory:

    mojibake_zip.py original.zip filename_encoding new.zip

Example usage, extract Japanese zipfile in Western European locale:

    mkdir temp
    cd temp
    mojibake_zip.py full_path_original.zip shiftjis full_path_new.zip
