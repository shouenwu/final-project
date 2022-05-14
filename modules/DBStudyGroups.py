from fastapi import HTTPException



from modules.ConnectToDatabase import ConnectToDatabase

import mariadb

def DBUserSearchStudentInGroup(board_id: int,
                               teacher_id: int,
                               student_account: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT study_groups.id,users.account \
            FROM study_groups \
            INNER JOIN users \
            ON study_groups.student_id =users.id\
            WHERE study_groups.teacher_id ={teacher_id} AND study_groups.board_id ={board_id} AND users.account LIKE '%{connection.escape_string(student_account)}%'"
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

def DBShowAllStudentsInGroup(board_id: int,
                             teacher_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT study_groups.id,users.account \
            FROM study_groups \
            INNER JOIN users \
            ON study_groups.student_id =users.id\
            WHERE study_groups.teacher_id ={teacher_id} AND study_groups.board_id ={board_id}"
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

def DBGetStudyGroup(study_group_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM study_groups \
            WHERE `id`={study_group_id}"
    study_group = {}

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, board_id,  teacher_id,  student_id, created_time) in cursor:

            study_group = {"id": id,
                    "board_id": board_id,
                    "teacher_id": teacher_id,
                    "student_id": student_id,
                    "created_time": created_time}

    finally:

        connection.close()

    if (study_group =={}):

        raise HTTPException(status_code = 404)

    return study_group

def DBCreateStudyGroup(board_id: int,
                   teacher_id: int,
                   student_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM study_groups \
            WHERE `board_id`={board_id} AND `teacher_id`={teacher_id} AND `student_id`={student_id}"
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

        raise HTTPException(status_code=400, detail="study_group already exists")

    connection, cursor = ConnectToDatabase()
    sql = f"INSERT INTO study_groups (`board_id`, `teacher_id`, `student_id`, `created_time`) \
            VALUES ('{board_id}', '{teacher_id}', '{student_id}', now())"

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

    return DBGetStudyGroup(study_group_id = study_group_id)

def DBDeleteStudyGroupByID(study_group_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM study_groups \
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
    
    sql = f"DELETE FROM study_groups \
            WHERE `id`={study_group_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return 

def DBDeleteStudyGroup(board_id: int,
                       student_id: int,
                       teacher_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"DELETE FROM study_groups \
            WHERE board_id={board_id} AND teacher_id={teacher_id} AND student_id={student_id}"

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

def DBGetBoardStudyGroup(board_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT teacher_id, student_id \
            FROM study_groups \
            WHERE board_id={board_id}"
    study_groups = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (teacher_id, student_id) in cursor:

            study_group = {"teacher": {"id": teacher_id},
                           "student": {"id": student_id}}
            study_groups.append(study_group)
        
    finally:

        connection.close()
    
    return study_groups

def DBCheckStudyGroup(board_id: int,
                      teacher_id: int,
                      student_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id\
            FROM study_groups \
            WHERE board_id = {board_id} AND teacher_id={teacher_id} AND student_id={student_id}"

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
    sql = f"SELECT id, board_id, teacher_id, student_id, created_time \
            FROM study_groups \
            WHERE `teacher_id`={teacher_id}"
    study_groups = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(sql)
        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (db_id, db_board_id, db_teacher_id, db_student_id, db_created_time) in cursor:

            study_group = {"id": db_id,
                           "board_id": db_board_id,
                           "teacher_id": db_teacher_id,
                           "student_id": db_student_id,
                           "created_time": db_created_time}
            
            study_groups.append(study_group)

    finally:

        connection.close()

    return study_groups

if __name__ == "__main__":

    pass
    #print(DBGetStudyGroup(study_group_id= 31))
    #print(DBCreateStudyGroup(board_id= 43,teacher_id= 2,student_id= 7))
    #DBDeleteStudyGroup(study_group_id= 31)
    #print(DBUserSearchStudentInGroup(board_id=43, teacher_id=2 ,student_account ="path"))#所有符合條件的account以及study_group_id
    #print(DBShowAllStudentsInGroup(board_id= 43,teacher_id= 2))#所有符合條件的account以及study_group_id
