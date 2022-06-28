from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException

from typing import Optional



from modules.CreateToken import CreateToken
from authentications.AuthUserMustBeTeacher import AuthUserMustBeTeacher
from authentications.AuthEditEbookPermission import AuthEditEbookPermission

import modules.DBEbookStudyGroups as DBEbookStudyGroup
import modules.DBUser as DBUser


router = APIRouter(
    tags = ["EbookStudyGroup"]
)


@router.get("/{ebook_id}")
async def ShowAllStudentsInGroup(ebook_id: int,
                        user: dict = Depends(AuthUserMustBeTeacher)):
    
    await AuthEditEbookPermission(ebook_id,
                                  user)
                       
    ebook_study_groups = DBEbookStudyGroup.DBShowAllStudentsInEbookStudyGroup(ebook_id = ebook_id,
                                                                              teacher_id =user['id'])
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebook_study_groups": ebook_study_groups}

@router.get("/{ebook_id}/users")
async def ShowAllUsersNotInGroup(ebook_id: int,
                        user: dict = Depends(AuthUserMustBeTeacher)):
    
    await AuthEditEbookPermission(ebook_id,
                                  user)
                       
    ebook_study_groups = DBEbookStudyGroup.DBShowAllStudentsNotInEbookStudyGroup(ebook_id = ebook_id,
                                                                              teacher_id =user['id'])

    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebook_study_groups": ebook_study_groups}

@router.post("/{ebook_id}")
async def PostEbookStudyGroup(ebook_id: int,
                         student_id: int,
                         user: dict = Depends(AuthUserMustBeTeacher)):

    await AuthEditEbookPermission(ebook_id,
                                  user)
            
    DBEbookStudyGroup.DBCreateEbookStudyGroup(ebook_id = ebook_id,
                                            teacher_id = user['id'],
                                            student_id = student_id)
    
    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}

@router.delete("/{ebook_id}/users/{student_id}")
async def DeleteEbookStudyGroupSingleUser(ebook_id: int,
                                     student_id: int,
                                     user: dict = Depends(AuthUserMustBeTeacher)):

    await AuthEditEbookPermission(ebook_id, user)                                     

    DBEbookStudyGroup.DBDeleteEbookStudyGroupbyAllInfo(ebook_id = ebook_id,
                                        student_id = student_id,
                                        teacher_id = user['id'])
        
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}