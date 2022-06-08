from fastapi import APIRouter
from fastapi import Depends

from fastapi.responses import FileResponse
from fastapi import Query
from typing import Optional



from modules.CreateToken import CreateToken

from authentications.AuthUserMustBeOnline import AuthUserMustBeOnline
from authentications.AuthUserMustBeTeacher import AuthUserMustBeTeacher

import modules.DBEbookTag as DBEbookTag
import modules.DBEbook as DBEbook
import modules.DBEbookPage as DBEbookPage



import json as JSON
import os




router = APIRouter(
    tags = ["CreateEbook"]
)

@router.post("/")
async def CreateEbook(title : str,
                      page_num: int,
                      tag: Optional[int] = None,
                      description: Optional[str] = "",
                      privacy: str = Query("private", regex = "^(private|public)$"),
                      user: dict = Depends(AuthUserMustBeTeacher)):


    if (tag == None):

        tag = "NULL"

    else:

        check_ebook_tag = DBEbookTag.DBGetEbookTag(ebook_tag_id=tag)


    ebook = DBEbook.DBCreateEbook(creator=user['id'],
                                  tag=tag,
                                  title=title,
                                  page_num=page_num,
                                  description=description,
                                  privacy=privacy,
                                  )

    ebook_id = ebook['id']

            
    #DBEbookPage.DBCreateButtonInitial(ebook=ebook_id,
    #                                      )

    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}
