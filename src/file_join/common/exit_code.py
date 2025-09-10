from enum import IntEnum, auto


class ExitCode(IntEnum):
    SUCCESS = auto()
    ILLEGAL_POS_TYPE = auto()
    NO_SUCH_FILE = auto()
    NO_OPTION_ARG = auto()
    ILLEGAL_OPTION_TYPE = auto()
    ILLEGAL_OPTION = auto()
    INSUFFICIENT_INPUT_FILES = auto()
    FILE_READ_ERR = auto()
    FILE_WRITE_ERR = auto()
