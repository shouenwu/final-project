from fastapi import Depends
from fastapi import HTTPException



from authentications.AuthUserMustBeOnline import AuthUserMustBeOnline



async def AuthUserMustBeStudent(user: dict = Depends(AuthUserMustBeOnline)):

    if (user["role"] == "student"):

        return user
    
    else:

        raise HTTPException(status_code = 403)
                            