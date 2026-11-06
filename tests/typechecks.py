from zipfile import ZIP_DEFLATED, ZipInfo

from typing_extensions import assert_type

import repro_zipfile
from repro_zipfile import ReproducibleZipFile, date_time, dir_mode, file_mode

assert_type(repro_zipfile.__version__, str)

# Metadata functions
assert_type(date_time(), tuple[int, int, int, int, int, int])
assert_type(file_mode(), int)
assert_type(dir_mode(), int)

# write, writestr, and mkdir
with ReproducibleZipFile("archive.zip", "w") as zf:
    assert_type(zf, ReproducibleZipFile)
    zf.write("file.txt")
    zf.write("file.txt", arcname="data.txt", compress_type=ZIP_DEFLATED, compresslevel=6)
    zf.writestr("data.txt", b"data")
    zf.writestr(ZipInfo("data.txt"), "data")
    zf.mkdir("dir")
    zf.mkdir(ZipInfo("dir/"), mode=0o755)
