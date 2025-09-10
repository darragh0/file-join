from dataclasses import dataclass, field
from typing import NotRequired, TypedDict

type OptionType = str | bool


class _Option(TypedDict):
    short: NotRequired[str]
    long: str
    type: type[OptionType]
    placeholder: NotRequired[str]
    help: str
    default: NotRequired[OptionType]


@dataclass
class _ParsedPos:
    files: list = field(default_factory=list)


@dataclass
class _ParsedOpt:
    force: bool = False
    verbose: bool = False
    output: str = "./joined.txt"
    no_quote: bool = False


@dataclass
class Parsed:
    pos: _ParsedPos = field(default_factory=_ParsedPos)
    opt: _ParsedOpt = field(default_factory=_ParsedOpt)


OPTIONS: list[_Option] = [
    {
        "short": "-o",
        "long": "--output",
        "type": str,
        "placeholder": "<file>",
        "help": "Output file",
        "default": "./joined.txt",
    },
    {
        "short": "-nq",
        "long": "--no-quote",
        "type": bool,
        "help": "Do not wrap file contents in code blocks",
        "default": False,
    },
    {
        "short": "-f",
        "long": "--force",
        "type": bool,
        "help": "Force overwrite of output file without prompt",
        "default": False,
    },
    {
        "long": "--verbose",
        "type": bool,
        "help": "Enable verbose output",
        "default": False,
    },
]

LONGEST_SHORT_OPT = max(len(opt.get("short", "")) for opt in OPTIONS)
