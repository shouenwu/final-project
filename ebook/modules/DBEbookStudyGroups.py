from fastapi import HTTPException
from modules.ConnectToDatabase import ConnectToDatabase
import mariadb

def DBUserSearchStudentInEbookStudyGroup(ebook_id: int,
                               teacher_id: int,
                               student_account: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT ebooks_study_groups.id,users.account \
            FROM ebooks_study_groups \
            INNER JOIN users \
            ON ebooks_study_groups.student_id =users.id\
            WHERE ebooks_study_groups.teacher_id ={teacher_id} AND ebooks_study_groups.ebook_id ={ebook_id} AND users.account LIKE '%{connection.escape_string(student_account)}%'"
    account_list = []
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id,account) in cursor:

            account = {"study_group_id": id,
                     "account" : account}
            account_list.append(account) 
    finally:

        connection.close()

    return account_list#所有符合條件的account以及study_group_id

def DBShowAllStudentsInEbookStudyGroup(ebook_id: int,
                             teacher_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT ebooks_study_groups.id,users.account \
            FROM ebooks_study_groups \
            INNER JOIN users \
            ON ebooks_study_groups.student_id =users.id\
            WHERE ebooks_study_groups.teacher_id ={teacher_id} AND ebooks_study_groups.ebook_id ={ebook_id}"
    account_list = []
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id,account) in cursor:

            account = {"study_group_id": id,
                     "account" : account}
            account_list.append(account) 
    finally:

        connection.close()

    return account_list#所有符合條件的account以及study_group_id

def DBGetEbookStudyGroupbyGroupID(study_group_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM ebooks_study_groups \
            WHERE `id`={study_group_id}"
    ebooks_study_group = {}

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, ebook_id,  teacher_id,  student_id, created_time) in cursor:

            ebooks_study_group = {"id": id,
                    "ebook_id": ebook_id,
                    "teacher_id": teacher_id,
                    "student_id": student_id,
                    "created_time": created_time}

    finally:

        connection.close()

    if (ebooks_study_group =={}):

        raise HTTPException(status_code = 404)

    return ebooks_study_group

def DBCreateEbookStudyGroup(ebook_id: int,
                   teacher_id: int,
                   student_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_study_groups \
            WHERE `ebook_id`={ebook_id} AND `teacher_id`={teacher_id} AND `student_id`={student_id}"
    whether_studygroup_exist = False

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id) in cursor:

            whether_studygroup_exist = True

    finally:

        connection.close()

    if (whether_studygroup_exist == True):

        raise HTTPException(status_code=400, detail="ebooks_study_group already exists")

    connection, cursor = ConnectToDatabase()
    sql = f"INSERT INTO ebooks_study_groups (`ebook_id`, `teacher_id`, `student_id`, `created_time`) \
            VALUES ('{ebook_id}', '{teacher_id}', '{student_id}', now())"

    study_group_id = None
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        study_group_id = cursor.lastrowid
    
    finally:

        connection.close()
    
    if (study_group_id == None):

        raise HTTPException(status_code = 404)

    return DBGetEbookStudyGroupbyGroupID(study_group_id = study_group_id)

def DBDeleteEbookStudyGroupByGroupID(study_group_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_study_groups \
            WHERE `id`={study_group_id}"
    whether_id_exist = False

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id) in cursor:

            whether_id_exist = True

    finally:

        connection.close()
    if (whether_id_exist == False):

        raise HTTPException(status_code=404, detail="study_group_id doesn't exist")

    connection, cursor = ConnectToDatabase()
    
    sql = f"DELETE FROM ebooks_study_groups \
            WHERE `id`={study_group_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return 

def DBDeleteEbookStudyGroupbyAllInfo(ebook_id: int,
                       student_id: int,
                       teacher_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"DELETE FROM ebooks_study_groups \
            WHERE ebook_id={ebook_id} AND teacher_id={teacher_id} AND student_id={student_id}"

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

def DBGetEbookStudyGroupbyEbookID(ebook_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT teacher_id, student_id \
            FROM ebooks_study_groups \
            WHERE ebook_id={ebook_id}"
    ebooks_study_groups = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (teacher_id, student_id) in cursor:

            ebooks_study_group = {"teacher": {"id": teacher_id},
                           "student": {"id": student_id}}
            ebooks_study_groups.append(ebooks_study_group)
        
    finally:

        connection.close()
    
    return ebooks_study_groups

def DBCheckEbookStudyGroup(ebook_id: int,
                      teacher_id: int,
                      student_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id\
            FROM ebooks_study_groups \
            WHERE ebook_id = {ebook_id} AND teacher_id={teacher_id} AND student_id={student_id}"

    data_id = None
    try: 

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (db_id) in cursor:

            data_id = db_id[0]
    
    finally:

        connection.close()
    
    return data_id

def DBGetStudentByTeacher(teacher_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, teacher_id, student_id, created_time \
            FROM ebooks_study_groups \
            WHERE `teacher_id`={teacher_id}"
    ebooks_study_groups = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(sql)
        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (db_id, db_ebook_id, db_teacher_id, db_student_id, db_created_time) in cursor:

            ebooks_study_group = {"id": db_id,
                           "ebook_id": db_ebook_id,
                           "teacher_id": db_teacher_id,
                           "student_id": db_student_id,
                           "created_time": db_created_time}
            
            ebooks_study_groups.append(ebooks_study_group)

    finally:

        connection.close()

    return ebooks_study_groups

if __name__ == "__main__":

    pass
    #print(DBGetEbookStudyGroupbyGroupID(study_group_id= 3))
    #print(DBCreateEbookStudyGroup(ebook_id= 2,teacher_id= 2,student_id= 9))
    #DBDeleteEbookStudyGroupByGroupID(study_group_id= 3)
    #print(DBUserSearchStudentInEbookStudyGroup(ebook_id=2, teacher_id=2 ,student_account =""))#所有符合條件的account以及study_group_id
    #print(DBShowAllStudentsInEbookStudyGroup(ebook_id= 2,teacher_id= 2))#所有符合條件的account以及study_group_id
