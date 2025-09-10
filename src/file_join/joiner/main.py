from datetime import datetime
from pathlib import Path

from file_join.common import ExitCode, Style, perr, psuccess, pwarn, yn_input


def _pifverbose(msg: str, verbose: bool) -> None:
    if verbose:
        print(msg)


def should_proceed(out: Path, *, force: bool, files: list[Path]) -> bool:
    if out.is_file() and not force:
        for file_path in files:
            if out.samefile(file_path):
                pwarn(
                    f"output file {Style.YLW}{out.name}{Style.RES} is also an input file! This may lead to weird behavior"
                )
                break
        else:
            pwarn(f"output file {Style.YLW}{out.name}{Style.RES} already exists!")

        ret = yn_input("override? (y/n): ")
        if ret:
            print()
        return ret

    return True


def join_files(out: Path, *, verbose: bool, files: list[Path], no_quote: bool) -> None:
    out.write_text("")
    first = True
    verbose = verbose
    quote = "" if no_quote else "```"

    for file_path in files:
        stats = file_path.stat()
        mtime = datetime.fromtimestamp(stats.st_mtime)

        _pifverbose(f"reading {Style.BLU}{file_path.name}{Style.RES} ...", verbose)
        _pifverbose(f"  last modified: {Style.CYN}{mtime}{Style.RES}", verbose)
        _pifverbose(f"  size: {Style.CYN}{stats.st_size:,} Bytes{Style.RES}", verbose)

        try:
            cont = file_path.read_text()
        except Exception:
            perr(
                f"failed to read file {Style.YLW}{file_path!s}{Style.RES}",
                ExitCode.FILE_READ_ERR,
            )
            assert False, "unreachable"

        _pifverbose("writing ...\n", verbose)

        pre = f"{'' if first else '\n'}##### FILE: {file_path.name}, LAST_MODIFIED: {mtime} #####\n{quote}\n"
        first = False

        try:
            with open(out, "a", encoding="utf-8") as file:
                file.write(f"{pre}{cont}{quote}\n")
        except Exception:
            perr(
                f"failed to open file {Style.YLW}{out!s}{Style.RES} for writing",
                ExitCode.FILE_WRITE_ERR,
            )

    psuccess(f"joined {len(files)} files into {Style.YLW}{out!s}{Style.RES}")
