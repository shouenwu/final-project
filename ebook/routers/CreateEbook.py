from fastapi import APIRouter
from fastapi import Depends
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from fastapi import Query
from typing import Optional
from fastapi.exceptions import HTTPException
import modules.FileImage as FileImage

from modules.CreateToken import CreateToken

from authentications.AuthUserMustBeOnline import AuthUserMustBeOnline
from authentications.AuthUserMustBeTeacher import AuthUserMustBeTeacher

import modules.DBEbookTag as DBEbookTag
import modules.DBEbook as DBEbook
import modules.DBEbookPage as DBEbookPage



import json as JSON
import os

PATH_PUBLIC = None
PATH_EBOOK_COVER_IMAGES = None

with open("./configs/global.json", "r") as file_input:
    config = JSON.load(file_input)
    PATH_PUBLIC = config["PATH_PUBLIC"]
    PATH_EBOOK_COVER_IMAGES = config["PATH_EBOOK_COVER_IMAGES"]


router = APIRouter(
    tags = ["CreateEbook"]
)

@router.post("/")
async def CreateEbook(title : str,
                      page_num: int,
                      tag: Optional[int] = None,
                      description: Optional[str] = "",
                      privacy: str = Query("private", regex = "^(private|public)$"),
                      file_input: UploadFile = File(...),
                      user: dict = Depends(AuthUserMustBeTeacher)):

    if (tag == None):

        tag = "NULL"

    else:

        DBEbookTag.DBGetEbookTag(ebook_tag_id=tag)
    
    file_type = file_input.content_type
    
    if(not file_type.startswith("image")):

        raise HTTPException(status_code = 403)


    ebook = DBEbook.DBCreateEbook(creator=user['id'],
                                  tag=tag,
                                  title=title,
                                  page_num=page_num,
                                  description=description,
                                  privacy=privacy,
                                  )

    ebook_id = ebook['id']

    file_name = f"{ebook_id}"
    

    await FileImage.CreateImage(path_image = os.path.join(PATH_PUBLIC, PATH_EBOOK_COVER_IMAGES),
                                path_user = str(user['id']),
                                image_name = file_name,
                                file_input = file_input)
    
    #DBEbookPage.DBCreateButtonInitial(ebook=ebook_id,)page initial
                                        

    token = CreateToken(user)
    return {"state": "success",
            "ebook": ebook,
            "access_token": token,
            "token_type": "bearer"}
