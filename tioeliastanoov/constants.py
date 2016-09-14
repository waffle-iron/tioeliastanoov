from enum import Enum


class TioEliasStatus(Enum):
    available = 1
    unavailable = 2
    maybe_available = 3
    maybe_unavailable = 4

