from fastapi import APIRouter
from fastapi import Depends
from fastapi import File, UploadFile
from fastapi import Query
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse

from typing import Optional



import mariadb
from modules.ConnectToDatabase import ConnectToDatabase



from modules.CreateToken import CreateToken

import modules.FileImage as FileImage
import modules.FileVoice as FileVoice
import modules.FileVideo as FileVideo
import modules.DBEbookImage as DBEbookImage
import modules.DBEbookPage as DBEbookPage
import modules.DBEbookVideo as DBEbookVideo
import modules.DBEbookVoice as DBEbookVoice
import modules.DBEbook as DBEbook



from authentications.AuthUserMustBeTeacher import AuthUserMustBeTeacher
from authentications.AuthEditEbookPermission import AuthEditEbookPermission



import json as JSON
import os



PATH_PUBLIC = None
PATH_EBOOK_IMAGES = None
PATH_EBOOK_VOICES = None
PATH_EBOOK_VIDEOS = None
with open("./configs/global.json", "r") as file_input:

    config = JSON.load(file_input)

    PATH_PUBLIC = config["PATH_PUBLIC"]
    PATH_EBOOK_IMAGES = config["PATH_EBOOK_IMAGES"]
    PATH_EBOOK_VOICES = config["PATH_EBOOK_VOICES"]
    PATH_EBOOK_VIDEOS = config["PATH_EBOOK_VIDEOS"]

router = APIRouter(
    tags = ["EditEbook"]
)

@router.get("/{ebook_id}")
async def GetEbook(ebook_id: int, user: dict = Depends(AuthUserMustBeTeacher)):

    await AuthEditEbookPermission(ebook_id,user)

    ebook = {"ebook_info": DBEbook.DBUseIdGetEbook(ebook_id = ebook_id)}

    pages = DBEbookPage.DBShowAllEbookPages(ebook_id = ebook_id)

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebook": ebook,
            "pages":pages}

@router.get("/images/search")
async def ShowAllEbookImages(ebook_id : int,
                            user: dict = Depends(AuthUserMustBeTeacher)):

    
    images = DBEbookImage.DBShowAllEbookImages(ebook_id = ebook_id)
    for image in images:
        del image['location']
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "images": images}

@router.get("/images/{ebook_id}")
async def EbookImagesDownload(ebook_image_id: int):

    image = DBEbookImage.DBUseIdGetEbookImage(ebook_image_id = ebook_image_id)

    image_dir = str(image["location"])
    ebook_dir = str(image['ebook_id'])
    path = os.path.join(PATH_PUBLIC, PATH_EBOOK_IMAGES, ebook_dir, image_dir)
    
    return FileResponse(path, media_type = "image/png")

@router.post("/images/upload")
async def EbookImagesUpload(ebook_id: int,
                            name: str,
                            file_input: UploadFile = File(...),
                            user: dict = Depends(AuthUserMustBeTeacher)):
    file_type = file_input.content_type
    
    await AuthEditEbookPermission(ebook_id,user)
    if(not file_type.startswith("image")):

        raise HTTPException(status_code = 403)

    image = DBEbookImage.DBCreateEbookImage(ebook_id = ebook_id,
                                            name = name)

    image_id = image['id']

    file_name = f"{image_id}"
    

    await FileImage.CreateImage(path_image = os.path.join(PATH_PUBLIC, PATH_EBOOK_IMAGES),
                                path_user = str(ebook_id),
                                image_name = file_name,
                                file_input = file_input)


    return {"state": "success",
            "image": image}

@router.get("/voices/search")
async def ShowAllEbookVoices(ebook_id : int,
                            user: dict = Depends(AuthUserMustBeTeacher)):

    voices = DBEbookVoice.DBShowAllEbookVoices(ebook_id = ebook_id)
    for voice in voices:
        del voice['location']
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "voices": voices}

@router.get("/voices/{ebook_id}")
async def EbookVoicesDownload(ebook_voice_id: int):

    voice = DBEbookImage.DBUseIdGetEbookImage(ebook_voice_id = ebook_voice_id)

    voice_dir = str(voice["location"])
    ebook_dir = str(voice['ebook_id'])
    path = os.path.join(PATH_PUBLIC, PATH_EBOOK_IMAGES, ebook_dir, voice_dir)
    
    return FileResponse(path, media_type = "voice/mp3")

@router.post("/voices/upload")
async def EbookVoicesUpload(ebook_id: int,
                            name: str,
                            file_input: UploadFile = File(...),
                            user: dict = Depends(AuthUserMustBeTeacher)):
    file_type = file_input.content_type
    await AuthEditEbookPermission(ebook_id,user)
    
    if(not file_type.startswith("voice")):

        raise HTTPException(status_code = 403)

    voice = DBEbookVoice.DBCreateEbookVoice(ebook_id = ebook_id,
                                            name = name)

    voice_id = voice['id']

    file_name = f"{voice_id}"
    

    await FileVoice.CreateVoice(path_image = os.path.join(PATH_PUBLIC, PATH_EBOOK_IMAGES),
                                path_ebook = str(ebook_id),
                                image_name = file_name,
                                file_input = file_input)

    return {"state": "success",
            "voice": voice}

@router.get("/videos/search")
async def ShowAllEbookVideos(ebook_id : int,
                            user: dict = Depends(AuthUserMustBeTeacher)):

    videos = DBEbookVoice.DBShowAllEbookVoices(ebook_id = ebook_id)
    for video in videos:
        del video['location']
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "videos": videos}

@router.get("/videos/{ebook_id}")
async def EbookVideosDownload(ebook_video_id: int):

    video = DBEbookVideo.DBUseIdGetEbookVideo(ebook_voice_id = ebook_video_id)

    video_dir = str(video["location"])
    ebook_dir = str(video['ebook_id'])
    path = os.path.join(PATH_PUBLIC, PATH_EBOOK_IMAGES, ebook_dir, video_dir)
    
    return FileResponse(path, media_type = "video/mp4")

@router.post("/videos/upload")
async def EbookVideosUpload(ebook_id: int,
                            name: str,
                            file_input: UploadFile = File(...),
                            user: dict = Depends(AuthUserMustBeTeacher)):
    file_type = file_input.content_type
    await AuthEditEbookPermission(ebook_id,user)
    
    if(not file_type.startswith("video")):

        raise HTTPException(status_code = 403)

    video = DBEbookVideo.DBCreateEbookVideo(ebook_id = ebook_id,
                                            name = name)

    video_id = video['id']

    file_name = f"{video_id}"
    

    await FileVideo.CreateVideo(path_image = os.path.join(PATH_PUBLIC, PATH_EBOOK_IMAGES),
                                path_ebook = str(ebook_id),
                                image_name = file_name,
                                file_input = file_input)

    return {"state": "success",
            "video": video}


