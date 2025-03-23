from zipfile import ZipFile, ZipInfo

from _typeshed import SizedBuffer, StrPath

__all__ = ["date_time", "file_mode", "dir_mode", "ReproducibleZipFile"]
__version__: str

def date_time() -> tuple[int, int, int, int, int, int]: ...
def file_mode() -> int: ...
def dir_mode() -> int: ...

class ReproducibleZipFile(ZipFile):
    def write(
        self,
        filename: StrPath,
        arcname: StrPath | None = None,
        compress_type: int | None = None,
        compresslevel: int | None = None,
    ) -> None: ...
    def writestr(
        self,
        zinfo_or_arcname: str | ZipInfo,
        data: SizedBuffer | str,
        compress_type: int | None = None,
        compresslevel: int | None = None,
    ) -> None: ...
    def mkdir(self, zinfo_or_directory_name: str | ZipInfo, mode: int = 511) -> None: ...
