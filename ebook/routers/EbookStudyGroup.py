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
async def GetEbookStudyGroup(ebook_id: int,
                        user: dict = Depends(AuthUserMustBeTeacher)):
    
    await AuthEditEbookPermission(ebook_id,
                                  user)
                       
    ebook_study_groups = DBEbookStudyGroup.DBGetEbookStudyGroupbyEbookID(ebook_id = ebook_id)
    
    for study_group in ebook_study_groups:

        teacher = DBUser.DBGetUser(user_id = study_group['teacher']['id'])
        del teacher['password']
        study_group['teacher'].update(teacher)

        student = DBUser.DBGetUser(user_id = study_group['student']['id'])
        del student['password']
        study_group['student'].update(student)

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

    data_id = DBEbookStudyGroup.DBCheckStudyGroup(ebook_id = ebook_id,
                                                 teacher_id = user['id'],
                                                 student_id = student_id)
    
    if (data_id == None):
            
        DBEbookStudyGroup.DBCreateStudyGroup(ebook_id = ebook_id,
                                            teacher_id = user['id'],
                                            student_id = student_id)
    
    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}

@router.get("/{ebook_id}/users/search")
async def GetSearchEbookStudyGroupSingleUser(ebook_id: int,
                                        account: str,
                                        user: dict = Depends(AuthUserMustBeTeacher)):
    
    await AuthEditEbookPermission(id = ebook_id, 
                                  user = user)
    
    users = DBUser.DBSearchUser(account = account)

    token = CreateToken(user)

    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "users": users}

@router.get("/{ebook_id}/users/{student_id}")
async def GetEbookStudyGroupSingleUser(ebook_id: int,
                                  student_id: int,
                                  user: dict = Depends(AuthUserMustBeTeacher)):

    await AuthEditEbookPermission(ebook_id, user)

    student = DBUser.DBGetUser(user_id = student_id)
    del student['password']
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "user": student}

@router.delete("/{ebook_id}/users/{student_id}")
async def DeleteStudyGroupSingleUser(ebook_id: int,
                                     student_id: int,
                                     user: dict = Depends(AuthUserMustBeTeacher)):

    await AuthEditEbookPermission(ebook_id, user)                                     

    DBEbookStudyGroup.DBDeleteStudyGroup(ebook_id = ebook_id,
                                        student_id = student_id,
                                        teacher_id = user['id'])
        
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer"}