from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException

from typing import Optional



from modules.CreateToken import CreateToken


from authentications.AuthUserMustBeOnline import AuthUserMustBeOnline
from authentications.AuthEditEbookTagPermission import AuthEditEbookTagPermission

import modules.DBEbookTag as DBEbookTag



router = APIRouter(
    tags = ["EbookTag"]
)

@router.get("/{tag_id}")
async def GetEbookTag(tag_id: int,
                      user: dict = Depends(AuthUserMustBeOnline)):

    await AuthEditEbookTagPermission(tag_id=tag_id,
                                     user=user)
    
    ebook_tag = DBEbookTag.DBGetEbookTag(ebook_tag_id=tag_id)

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebook_tag": ebook_tag}

@router.put("/{tag_id}")
async def PutEbookTag(tag_id: int,
                      name: Optional[str] = "",
                      description: Optional[str] = "",
                      user: dict = Depends(AuthUserMustBeOnline)):

    await AuthEditEbookTagPermission(tag_id = tag_id,
                                     user = user)

    DBEbookTag.DBEditEbookTag(ebook_tag_id=tag_id,
                              name=name,
                              description=description)

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}

@router.delete("/{tag_id}")
async def DeleteEbookTag(tag_id: int,
                         user: dict = Depends(AuthUserMustBeOnline)):

    await AuthEditEbookTagPermission(tag_id=tag_id,
                                     user=user)
    
    DBEbookTag.DBDeleteBoardTag(ebook_tag_id=tag_id)

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}

@router.get("/")
async def GetEbookTagAll(user: dict = Depends(AuthUserMustBeOnline)):

    ebook_tags = DBEbookTag.DBShowAllUserEbookTag(creator=user['id'])

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebook_tags": ebook_tags}

@router.post("/")
async def PostEbookTag(name: str,
                       description: Optional[str] = "",
                       user: dict = Depends(AuthUserMustBeOnline)):

    ebook_tag = DBEbookTag.DBCreateEbookTag(creator=user['id'],
                                            name=name,
                                            description=description)

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebook_tag": ebook_tag}
