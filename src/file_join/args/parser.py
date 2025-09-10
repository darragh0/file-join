from pathlib import Path
from sys import argv
from sys import exit as sys_exit

from file_join.args.msg import show_help, show_ver
from file_join.args.spec import OPTIONS, OptionType, Parsed
from file_join.common import ExitCode, Style, perr


def _parse_opt(arg: str, arg_i: int, argc: int) -> tuple[str, OptionType]:
    for opt in OPTIONS:
        if arg in (opt.get("short"), opt["long"]):
            req_type = opt["type"]
            name = opt["long"].lstrip("-")

            if req_type is bool:
                return name.replace("-", "_"), True

            val_i = arg_i + 1
            if not val_i < argc:
                perr(
                    f"option requires argument -- {Style.YLW}{arg}{Style.RES}",
                    ExitCode.NO_OPTION_ARG,
                )

            val = argv[arg_i + 1]
            if not isinstance(val, req_type):
                perr(
                    f"illegal type for {Style.YLW}{arg}{Style.RES}: expected {Style.YLW}{req_type.__name__}"
                    f"{Style.RES}, got {Style.YLW}{type(val).__name__}{Style.RES}",
                    ExitCode.ILLEGAL_OPTION_TYPE,
                )

            return name.replace("-", "_"), val

    perr(f"illegal option -- {Style.YLW}{arg}{Style.RES}", ExitCode.ILLEGAL_OPTION)
    assert False, "unreachable"


def parse_args() -> Parsed:
    parsed = Parsed()
    argc = len(argv)
    accounted_for = set()

    # Print help and/or version (disregard all other args)
    shown_ver = False
    vh = "-vh" in argv or "-hv" in argv
    if vh or ("-v" in argv or "--version" in argv):
        show_ver()
        shown_ver = True

    if vh or "-h" in argv or "--help" in argv:
        show_help()
        sys_exit(0)

    if shown_ver:
        sys_exit(0)

    for arg_i, arg in enumerate(argv[1:], 1):
        if arg_i in accounted_for:
            continue

        if arg.startswith(("-", "--")):
            name, val = _parse_opt(arg, arg_i, argc)
            setattr(parsed.opt, name, val)
            if not isinstance(val, bool):
                accounted_for.add(arg_i + 1)
            continue

        req_type = "file_name"
        if not isinstance(arg, str):
            perr(
                f"illegal type for {Style.YLW}{arg}{Style.RES}: expected {Style.YLW}{req_type}"
                f"{Style.RES}, got {Style.YLW}{type(arg).__name__}{Style.RES}",
                ExitCode.ILLEGAL_POS_TYPE,
            )

        if not Path(arg).is_file():
            perr(
                f"no such file -- {Style.YLW}{arg}{Style.RES}",
                ExitCode.NO_SUCH_FILE,
            )

        parsed.pos.files.append(Path(arg).resolve())

    if (ln := len(parsed.pos.files)) < 2:
        perr(
            f"at least {Style.BLU}2{Style.RES} input files are required, got {Style.BLU}{ln}{Style.RES}",
            ExitCode.INSUFFICIENT_INPUT_FILES,
        )

    return parsed
