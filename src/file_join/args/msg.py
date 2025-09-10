from file_join import __description__, __prog__, __version__
from file_join.args.spec import LONGEST_SHORT_OPT, OPTIONS
from file_join.common import Style


def _show_arg_desc(arg_str: str, desc: str, indent: int, ansi_offset: int = 0) -> None:
    ljust = 25
    ansi_offset += 9
    sep = " " * (ljust - len(arg_str) + ansi_offset)

    print(f"{' ' * indent}{Style.CYN}{arg_str}{Style.RES}", end="")
    print(f"{sep}{desc}")


def show_help() -> None:
    indent = 2
    sl_sep = f" {Style.DIM}/{Style.RES}{Style.CYN} "
    sl_sep_ansi_offset = 13

    print(f"{__description__}\n\n{Style.BLD}{Style.MAG}Args:{Style.RES}")

    _show_arg_desc(
        f"file1 file2 {Style.DIM}[file3 ...]",
        "Files to be concatenated",
        indent,
        ansi_offset=4,
    )

    print(f"\n{Style.BLD}{Style.MAG}Options:{Style.RES}")
    for opt in OPTIONS:
        ansi_offset = 0
        if _short := opt.get("short"):
            short = f"{_short:<{LONGEST_SHORT_OPT}}{sl_sep}"
            ansi_offset += sl_sep_ansi_offset
        else:
            short = " " * (LONGEST_SHORT_OPT + len(sl_sep) - sl_sep_ansi_offset)

        placeholder = (
            f" {Style.DIM}{opt.get('placeholder')}" if opt.get("placeholder") else ""
        )

        if placeholder:
            ansi_offset += 4

        help = opt["help"]
        default = opt.get("default", None)
        if default is not None and not isinstance(default, bool):
            is_str = isinstance(default, str)
            quote = '"' if is_str and not default.startswith("./") else ""
            default_str = str(default).lower() if not is_str else default
            help += f" (default: {Style.YLW}{quote}{default_str}{quote}{Style.RES})"

        _show_arg_desc(
            f"{short}{opt['long']}{placeholder}", help, indent, ansi_offset=ansi_offset
        )

    print()


def show_ver() -> None:
    print(f"{Style.GRN}{__prog__}{Style.RES} v{__version__}")
