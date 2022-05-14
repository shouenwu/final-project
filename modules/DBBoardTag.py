import mariadb
from fastapi import HTTPException
from modules.ConnectToDatabase import ConnectToDatabase

def DBUserSearchBoardTag(creator: int,
                         name: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, description, created_time \
            FROM board_tags \
            WHERE name LIKE '%{connection.escape_string(name)}%' AND creator ={creator}"
    board_tags = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, name, description, created_time) in cursor:

            board_tag = {"id": id,
                    "creator": creator,
                    "name": name,
                    "description": description,
                    "created_time": created_time}
            board_tags.append(board_tag)

    finally:

        connection.close()

    return board_tags

def DBShowAllUserBoardTag(creator: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, description, created_time \
            FROM board_tags \
            WHERE creator ={creator}"
    board_tags = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, name, description, created_time) in cursor:

            board_tag = {"id": id,
                    "creator": creator,
                    "name": name,
                    "description": description,
                    "created_time": created_time}
            board_tags.append(board_tag)

    finally:

        connection.close()

    return board_tags

def DBGetBoardTag(board_tag_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, description, created_time \
            FROM board_tags \
            WHERE `id`={board_tag_id}"
    board_tag = {}

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator,  name,  description, created_time) in cursor:

            board_tag = {"id": id,
                    "creator": creator,
                    "name": name,
                    "description": description,
                    "created_time": created_time}

    finally:

        connection.close()

    if (board_tag =={}):

        raise HTTPException(status_code = 404)

    return board_tag

def DBCreateBoardTag(creator: int,
                   name: str,
                   description: str):

    connection, cursor = ConnectToDatabase()
    sql = f"INSERT INTO board_tags (`creator`, `name`, `description`, `created_time`) \
            VALUES ('{creator}', '{connection.escape_string(name)}', '{connection.escape_string(description)}', now())"

    board_tag_id = None
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        board_tag_id = cursor.lastrowid
    
    finally:

        connection.close()
    
    if (board_tag_id == None):

        raise HTTPException(status_code = 404)

    return DBGetBoardTag(board_tag_id = board_tag_id)

def DBEditBoardTag(board_tag_id: int,
                  name: str,
                  description: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM board_tags \
            WHERE `id`={board_tag_id}"
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

        raise HTTPException(status_code=404, detail="id doesn't exist")

    connection, cursor = ConnectToDatabase()
    sql = f"UPDATE board_tags \
            SET `name`='{connection.escape_string(name)}', \
                `description`='{connection.escape_string(description)}' \
            WHERE`id`={board_tag_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return DBGetBoardTag(board_tag_id = board_tag_id)

def DBDeleteBoardTag(board_tag_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM board_tags \
            WHERE `id`={board_tag_id}"
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

        raise HTTPException(status_code=404, detail="id doesn't exist")

    connection, cursor = ConnectToDatabase()
    
    sql = f"DELETE FROM board_tags \
            WHERE `id`={board_tag_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return 

if __name__ == "__main__":

    pass
    #print(DBUserSearchBoardTag(creator = 1,name = "b"))
    #print(DBShowAllUserBoardTag(creator = 1))
    #print(DBGetBoardTag(board_tag_id= 16))
    #print(DBCreateBoardTag(creator= 1,name= "testing",description= "for test"))
    #print(DBEditBoardTag(board_tag_id= 18,name= "b",description= "for test"))
    #DBDeleteBoardTag(board_tag_id= 16)