from enum import Enum


class TioEliasStatus(Enum):
    available = 1
    unavailable = 2
    maybe_available = 3
    maybe_unavailable = 4

    def to_message(self):
        return MESSAGES[self]


MESSAGES = {
    TioEliasStatus.available: 'Sim! \o/',
    TioEliasStatus.unavailable: 'Não =(',
    TioEliasStatus.maybe_available: 'Provavelmente sim ¯\_(ツ)_/¯',
    TioEliasStatus.maybe_unavailable: 'Provavelmente não ¯\_(ツ)_/¯',
}

