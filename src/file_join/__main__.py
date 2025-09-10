from datetime import datetime
from pathlib import Path
from sys import exit as sys_exit

from file_join.args import parse_args
from file_join.common import ExitCode, Style, perr, psuccess, pwarn, yn_input


def main() -> None:
    args = parse_args()

    out = Path(args.opt.output).resolve()
    proceed = True
    if out.is_file() and not args.opt.force:
        for file_path in args.pos.files:
            if out.samefile(file_path):
                pwarn(
                    f"output file {Style.YLW}{out.name}{Style.RES} is also an input file! This may lead to weird behavior"
                )
                break
        else:
            pwarn(f"output file {Style.YLW}{out.name}{Style.RES} already exists!")

        proceed = yn_input("override? (y/n): ")

    if not proceed:
        sys_exit(0)

    out.write_text("")
    first = True
    for file_path in args.pos.files:
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

        if args.opt.verbose:
            print("reading", Style.YLW + file_path.name + Style.RES, "...")

        try:
            cont = file_path.read_text()
        except Exception:
            perr(
                f"failed to read file {Style.YLW}{file_path!s}{Style.RES}",
                ExitCode.FILE_READ_ERR,
            )
            assert False, "unreachable"

        if args.opt.verbose:
            print("writing", Style.YLW + file_path.name + Style.RES, "...")

        pre = f"{'' if first else '\n'}# ---- {file_path.name} (last modified: {mtime}) ---- #\n```\n"
        first = False

        try:
            with open(out, "a", encoding="utf-8") as file:
                file.write(f"{pre}{cont}```\n")
        except Exception:
            perr(
                f"failed to open file {Style.YLW}{out!s}{Style.RES} for writing",
                ExitCode.FILE_WRITE_ERR,
            )

    print()
    psuccess(f"joined {len(args.pos.files)} files into {Style.YLW}{out!s}{Style.RES}")


if __name__ == "__main__":
    main()
