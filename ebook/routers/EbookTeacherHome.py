from fastapi import APIRouter
from fastapi import Depends


import modules.FileImage as FileImage
from modules.CreateToken import CreateToken
from fastapi.responses import FileResponse
from authentications.AuthUserMustBeOnline import AuthUserMustBeOnline
from authentications.AuthUserMustBeTeacher import AuthUserMustBeTeacher
from authentications.AuthEditEbookPermission import AuthEditEbookPermission

import modules.DBUser as DBUser
import modules.DBEbook as DBEbook
import modules.DBEbookTag as DBEbookTag


import modules.FileVoice as FileVoice



import json as JSON
import os



PATH_PUBLIC = None
PATH_EBOOK_COVER_IMAGES = None

with open("./configs/global.json", "r") as file_input:
    config = JSON.load(file_input)
    PATH_PUBLIC = config["PATH_PUBLIC"]
    PATH_EBOOK_COVER_IMAGES = config["PATH_EBOOK_COVER_IMAGES"]

router = APIRouter(
    tags = ["EbookTeacherHome"]
)



@router.get("/")
async def EbookTeacherHome(user: dict = Depends(AuthUserMustBeTeacher)):

    user_data = DBUser.DBGetUser(user_id = user["id"])
    user_data.pop("password")

    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "user": user_data}

@router.delete("/ebooks/private/{ebook_id}")
async def EbookTeacherHomeEbookPrivateDeleteSingleEbook(ebook_id: int,
                                                   user: dict = Depends(AuthUserMustBeOnline)):

    await AuthEditEbookPermission(ebook_id, user)
    file_name = f"{ebook_id}"
    
    FileImage.DeleteImage(path_image = os.path.join(PATH_PUBLIC, PATH_EBOOK_COVER_IMAGES),
                                path_user = str(user['id']),
                                image_name = file_name)
                                
    # delete image file
    #buttons = DBButton.DBShowAllEbookButtons(ebook_id=ebook_id)

    # delete database ebook data
    DBEbook.DBDeleteEbook(ebook_id=ebook_id)

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}

@router.get("/ebooks/private")
async def EbookTeacherHomeEbookPrivate(user: dict = Depends(AuthUserMustBeTeacher)):
    
    ebooks = DBEbook.DBShowAllUserCreateEbook(creator=user['id'])

    for ebook in ebooks:
        
        temp_tag = ebook['tag']
        if (temp_tag != None):
            
            tag = DBEbookTag.DBGetEbookTag(ebook_tag_id=temp_tag)
            ebook['tag'] = {"id": temp_tag}
            ebook['tag'].update(tag)
        
        else:

            ebook['tag'] = {"id": None}

    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebooks": ebooks}

@router.get("/ebooks/public")
async def EbookTeacherHomeEbookPublic(user: dict = Depends(AuthUserMustBeTeacher)):
    
    ebooks = DBEbook.DBShowAllPublicEbook()
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebooks": ebooks}

@router.get("/ebook_cover_image/{ebook_id}/download")
async def EbookCoverImageDownload(ebook_id: int):

    ebook = DBEbook.DBUseIdGetEbook(ebook_id = ebook_id)

    image_dir = str(ebook['cover_image_location'])
    user_dir = str(ebook['creator'])
    path = os.path.join(PATH_PUBLIC, PATH_EBOOK_COVER_IMAGES, user_dir, image_dir)
    return FileResponse(path, media_type = "image/png")
            
