from enum import Enum


class IGenderEnum(str, Enum):
    female = "female"
    male = "male"
    other = "other"


class IOrderStatus(str, Enum):
    processing = "processing"
    sent = "sent"
    delivered = "delivered"

