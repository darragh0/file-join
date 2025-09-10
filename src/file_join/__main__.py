from pathlib import Path

from file_join.args import parse_args
from file_join.joiner import join_files, should_proceed


def main() -> None:
    args = parse_args()
    out = Path(args.opt.output).resolve()

    if not should_proceed(out, force=args.opt.force, files=args.pos.files):
        return

    join_files(
        out,
        verbose=args.opt.verbose,
        files=args.pos.files,
        no_quote=args.opt.no_quote,
    )


if __name__ == "__main__":
    main()
