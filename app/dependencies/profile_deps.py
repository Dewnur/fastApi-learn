from uuid import UUID

from fastapi import Depends

from app.api.deps import get_model_by_id, get_current_user
from app.models import Profile, User
from app.utils.exceptions.auth_exception import InvalidTokenException
from app.utils.exceptions.profile_exception import MissingPhoneNumberException, MissingAddressException


def validate_user_profile():
    async def get_profile(
            profile_id: UUID,
            current_user: User = Depends(get_current_user())
    ):
        profile: Profile = await get_model_by_id(obj_id=profile_id, model=Profile)

        if profile.id != current_user.profile.id:
            raise InvalidTokenException()
        if not profile.phone_number:
            raise MissingPhoneNumberException()
        if not profile.address:
            raise MissingAddressException()

        return profile

    return get_profile
