from fastapi import Depends
from fastapi import HTTPException



from authentications.AuthUserMustBeOnline import AuthUserMustBeOnline



async def AuthUserMustBeTeacher(user: dict = Depends(AuthUserMustBeOnline)):

    if (user["role"] == "teacher"):

        return user
    
    else:

        raise HTTPException(status_code = 403)
    