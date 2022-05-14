import mariadb
from fastapi import HTTPException
from modules.ConnectToDatabase import ConnectToDatabase

def DBSearchAllBoardIcon():

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, description, location, created_time \
            FROM board_icons"
    board_icons = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, location, name, description, created_time) in cursor:

            board_icon = {"id": id,
                          "name": name,
                          "description": description,
                          "location": location,
                          "created_time": created_time}
            board_icons.append(board_icon)

    finally:

        connection.close()

    return board_icons

def DBSearchBoardIcon(name: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, description, location, created_time \
            FROM board_icons \
            WHERE name LIKE '%{connection.escape_string(name)}%'"
    board_icons = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, location, name, description, created_time) in cursor:

            board_icon = {"id": id,
                          "name": name,
                          "description": description,
                          "location": location,
                          "created_time": created_time}
            board_icons.append(board_icon)

    finally:

        connection.close()

    return board_icons

def DBGetBoardIcon(board_icon_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, description, location, created_time \
            FROM board_icons \
            WHERE `id`={board_icon_id}"
    board_icon = {}

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, name, description, location, created_time) in cursor:

            board_icon = {"id": id,
                          "location": location,
                          "name": name,
                          "description": description,
                          "created_time": created_time}

    finally:

        connection.close()

    if (board_icon =={}):

        raise HTTPException(status_code = 404)

    return board_icon

def DBCreateBoardIcon(name: str,
                     description: str):
    location = "unknown"                                                               
    connection, cursor = ConnectToDatabase()
    if(description == ""):

        sql = f"INSERT INTO board_icons ( `name`, `description`,`location`, `created_time`) \
                VALUES ( '{connection.escape_string(name)}', NULL ,'{connection.escape_string(location)}', now())"
    else:

        sql = f"INSERT INTO board_icons ( `name`, `description`,`location`, `created_time`) \
                VALUES ( '{connection.escape_string(name)}', '{connection.escape_string(description)}','{connection.escape_string(location)}', now())"
    board_icon_id = None
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        board_icon_id = cursor.lastrowid
    
    finally:

        connection.close()
    
    if (board_icon_id == None):

        raise HTTPException(status_code = 404)
    location = str(board_icon_id) + ".png"
    connection, cursor = ConnectToDatabase()
    sql = f"UPDATE board_icons \
            SET `location`='{connection.escape_string(location)}' \
            WHERE`id`={board_icon_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()
        
    return DBGetBoardIcon(board_icon_id = board_icon_id)

def DBEditBoardIcon(board_icon_id: int,
                  name: str,
                  description: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM board_icons \
            WHERE `id`={board_icon_id}"
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
    if(description == ""):

        sql = f"UPDATE board_icons \
                SET `name`='{connection.escape_string(name)}', \
                    `description`=NULL \
                WHERE`id`={board_icon_id}"
    else:

        sql = f"UPDATE board_icons \
                SET `name`='{connection.escape_string(name)}', \
                    `description`='{connection.escape_string(description)}' \
                WHERE`id`={board_icon_id}"
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return DBGetBoardIcon(board_icon_id = board_icon_id)

def DBDeleteBoardIcon(board_icon_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM board_icons \
            WHERE `id`={board_icon_id}"
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
    
    sql = f"DELETE FROM board_icons \
            WHERE `id`={board_icon_id}"
    
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
    #print(DBSearchBoardIcon(name = "default"))
    #print(DBGetBoardIcon(board_icon_id= 0))
    #print(DBSearchAllBoardIcon())
    #print(DBCreateBoardIcon(name= "shouencreated",description= "abc123"))
    #print(DBEditBoardIcon(board_icon_id= 10,name= "shouen",description= ""))
    #DBDeleteBoardIcon(board_icon_id= 7)