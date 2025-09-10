from pathlib import Path
from sys import argv, stderr
from sys import exit as sys_exit

from file_join.common.style import Style


def get_cmd() -> str:
    return Path(argv[0]).name


def _pusage() -> None:
    cmd = get_cmd()
    print(
        f"\n{Style.BLD}{Style.MAG}Usage: {Style.CYN}{cmd}{Style.RES} {Style.CYN}{Style.DIM}"
        f"[options]{Style.RES}{Style.CYN} file1 file2 {Style.DIM}[file3 ...]{Style.RES}",
        f"\n\nSee {Style.BLD}{Style.CYN}{cmd}{Style.RES} {Style.CYN}--help{Style.RES} for more information",
        file=stderr,
    )


def perr(msg: str, exit_code: int | None = None) -> None:
    print(
        f"{Style.BLD}{Style.RED}error:{Style.RES} {msg}",
        file=stderr,
    )

    _pusage()

    if exit_code is not None:
        sys_exit(exit_code)


def pwarn(msg: str) -> None:
    print(f"{Style.BLD}{Style.YLW}warning:{Style.RES} {msg}")


def psuccess(msg: str) -> None:
    print(f"{Style.BLD}{Style.GRN}success:{Style.RES} {msg}")


def yn_input(prompt: str) -> bool:
    meow = True
    while True:
        choice = input(prompt)
        if choice in {"y", "yes"}:
            return True
        elif choice in {"n", "no"}:
            return False
        print("\033[F\033[2K\r", end="")
        if meow:
            prompt = f"{Style.RED}x{Style.RES} {prompt}"
            meow = False
