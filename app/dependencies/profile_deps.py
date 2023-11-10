from uuid import UUID

from app.api.deps import get_model_by_id
from app.models import Profile
from app.utils.exceptions.auth_exception import InvalidTokenException
from app.utils.exceptions.profile_exception import MissingPhoneNumberException, MissingAddressException


def validate_user_profile(profile: Profile, profile_by_id: Profile):
    if profile.id != profile_by_id.id:
        raise InvalidTokenException()
    if not profile.phone_number:
        raise MissingPhoneNumberException()
    if not profile.address:
        raise MissingAddressException()


async def profile_id_existing(profile_id: UUID):
    return await get_model_by_id(obj_id=profile_id, model=Profile)