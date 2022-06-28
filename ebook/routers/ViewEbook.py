from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, StreamingResponse



from modules.CreateToken import CreateToken

from authentications.AuthUserMustBeOnline import AuthUserMustBeOnline
from authentications.AuthViewEbookPermission import AuthViewEbookPermission


import modules.DBEbook as DBEbook
import modules.DBEbookPage as DBEbookPage
import modules.DBEbookImage as DBEbookImage
import modules.DBEbookTexts as DBEbookTexts
import modules.DBEbookVoice as DBEbookVoice
import modules.DBEbookVideo as DBEbookVideo



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
    tags = ["ViewEbook"]
)

@router.get("/{ebook_id}")
async def ViewEbook(ebook_id: int, user: dict = Depends(AuthUserMustBeOnline)):

    await AuthViewEbookPermission(ebook_id, user)

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
                            user: dict = Depends(AuthUserMustBeOnline)):

    await AuthViewEbookPermission(ebook_id, user)
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

router.get("/voices/search")
async def ShowAllEbookVoices(ebook_id : int,
                            user: dict = Depends(AuthUserMustBeOnline)):
    await AuthViewEbookPermission(ebook_id, user)
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

@router.get("/videos/search")
async def ShowAllEbookVideos(ebook_id : int,
                            user: dict = Depends(AuthUserMustBeOnline)):
    await AuthViewEbookPermission(ebook_id, user)
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

@router.get("/texts/search")
async def ShowAllEbookTexts(ebook_id : int,
                            user: dict = Depends(AuthUserMustBeOnline)):
    await AuthViewEbookPermission(ebook_id, user)
    texts = DBEbookTexts.DBShowAllEbookTexts(ebook_id = ebook_id)
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "videos": texts}
