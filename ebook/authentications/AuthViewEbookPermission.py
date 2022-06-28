import mariadb
from fastapi.exceptions import HTTPException



from modules.ConnectToDatabase import ConnectToDatabase
import modules.DBEbook as DBEbook


async def AuthViewEbookPermission(id: int, user: dict):

    if (user["role"] == "teacher"):

        ebook = DBEbook.DBUseIdGetEbook(ebook_id = id)

        if (ebook["privacy"] == "private"
            and ebook['creator'] == user['id']):

            return 
        
        elif (ebook["privacy"] == "public"):

            return 

        else:

            raise HTTPException(status_code= 403)
        
    elif (user["role"] == "student"):

        connection, cursor = ConnectToDatabase()
        sql = f"SELECT student_id \
                FROM ebooks_study_groups \
                WHERE ebook_id={id}"
        student_ids = []

        try:

            cursor.execute(sql)
        
        except mariadb.Error as e:

            print(e)
            raise HTTPException(status_code = 500)
        
        else:

            for (student_id) in cursor:

                student_ids.append(student_id[0])
            
        finally:

            connection.close()

        if (user["id"] not in student_ids):

            raise HTTPException(status_code = 403)

