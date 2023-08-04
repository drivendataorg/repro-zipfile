from pathlib import Path
from zipfile import ZipFile, ZipInfo

__version__ = "0.1"


class ReproducibleZipFile(ZipFile):
    def write(self, filename, arcname=None, compress_type=None, compresslevel=None):
        if arcname is None:
            arcname = filename

        self.writestr(
            zinfo_or_arcname=str(arcname),
            data=Path(filename).read_bytes(),
            compress_type=compress_type,
            compresslevel=compresslevel,
        )

    def writestr(self, zinfo_or_arcname, data, compress_type=None, compresslevel=None):
        if not isinstance(zinfo_or_arcname, ZipInfo):
            zinfo = ZipInfo(filename=zinfo_or_arcname, date_time=(1980, 1, 1, 0, 0, 0))
            zinfo.compress_type = self.compression
            zinfo._compresslevel = self.compresslevel
            if zinfo.filename.endswith("/"):
                zinfo.external_attr = 0o40775 << 16  # drwxrwxr-x
                zinfo.external_attr |= 0x10  # MS-DOS directory flag
            else:
                zinfo.external_attr = 0o600 << 16  # ?rw-------
        else:
            zinfo = ZipInfo(filename=zinfo_or_arcname.filename, date_time=(1980, 1, 1, 0, 0, 0))

        super().writestr(
            zinfo, data=data, compress_type=compress_type, compresslevel=compresslevel
        )

        self.filelist = sorted(self.filelist, key=lambda zinfo: zinfo.filename)
