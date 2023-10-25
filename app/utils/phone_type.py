from pydantic_extra_types.phone_numbers import PhoneNumber


class PhoneType(PhoneNumber):
    phone_format: str = 'E164'
