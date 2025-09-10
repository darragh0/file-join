from enum import StrEnum


class Style(StrEnum):
    # Text Styles
    BLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    BLU = "\033[94m"
    MAG = "\033[95m"
    CYN = "\033[96m"
    RES = "\033[0m"
