from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException

import mariadb



from modules.CreateToken import CreateToken
from modules.ConnectToDatabase import ConnectToDatabase

from authentications.AuthUserMustBeStudent import AuthUserMustBeStudent

import modules.DBUser as DBUser



router = APIRouter(
    tags = ["EbookStudentHome"]
)


@router.get("/")
async def EbookStudentHome(user: dict = Depends(AuthUserMustBeStudent)):

    user_data = DBUser.DBGetUser(user_id = user['id'])
    
    user_data.pop("password")
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "user": user_data}

@router.get("/ebooks/")
async def EbookStudentHomeEbooks(user: dict = Depends(AuthUserMustBeStudent)):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT ebooks.id, title, cover_image_location \
            FROM ebooks \
            INNER JOIN ebooks_study_groups ON ebooks_study_groups.ebook_id=ebooks.id\
            WHERE student_id={user['id']}"
    ebooks = []

    try:
        
        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (ebook_id, name, icon) in cursor:
            
            ebook = {"id": ebook_id,
                     "title": name,
                     "cover_image_location": icon}
            ebooks.append(ebook)

    finally:

        connection.close()
    
    token = CreateToken(user)
    return {"state": "success",
            "access_token": token,
            "token_type": "bearer",
            "ebooks": ebooks}
