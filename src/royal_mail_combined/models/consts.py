from enum import StrEnum


class SendNotifcationsTo(StrEnum):
    SENDER = 'sender'
    RECIPIENT = 'recipient'
    BILLING = 'billing'
