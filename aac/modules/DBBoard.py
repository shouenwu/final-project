from fastapi import HTTPException



import mariadb



from modules.ConnectToDatabase import ConnectToDatabase



def DBUserSearchALLBoard(creator: int,
                    name: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE name LIKE '%{connection.escape_string(name)}%'AND (creator={creator} OR privacy = 'public')"
    boards = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}
            boards.append(board)

    finally:

        connection.close()

    return boards

def DBShowUserAllBoard(creator: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE creator={creator} OR privacy = 'public'"
    boards = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}
            boards.append(board)

    finally:

        connection.close()
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE name LIKE '%{connection.escape_string(name)}%'AND privacy= 'public'"

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}
            boards.append(board)

    finally:

        connection.close()

    return boards

def DBShowAllUserCreateBoard(creator: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE creator={creator}"
    boards = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}
            boards.append(board)

    finally:

        connection.close()
    return boards

def DBShowAllPublicBoard():
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE privacy= 'public'"
    boards = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}
            boards.append(board)

    finally:

        connection.close()
    return boards

def DBSearchPublicBoard(name: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE privacy= 'public' AND name LIKE '%{connection.escape_string(name)}%'"
    boards = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}
            boards.append(board)

    finally:

        connection.close()
    return boards

def DBSearchUserCreateBoard(creator: int,
                        name: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE `creator`={creator} AND name LIKE '%{connection.escape_string(name)}%'"
    boards = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}
            boards.append(board)

    finally:

        connection.close()
    return boards

def DBUseIdGetBoard(board_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time \
            FROM boards \
            WHERE id = {board_id}"
    board = {}

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, name, row_size, column_size, description, privacy, icon, is_label_enable, created_time) in cursor:

            board = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "name": name,
                    "row_size": row_size,
                    "column_size": column_size,
                    "description": description,
                    "privacy": privacy,
                    "icon": icon,
                    "is_label_enable": is_label_enable,
                    "created_time": created_time}

    finally:

        connection.close()

    if (board =={}):

        raise HTTPException(status_code = 404)

    return board

def DBCreateBoard(creator: int,
                 tag: int,
                 name: str,
                 row_size: int,
                 column_size: int,
                 description: str,
                 privacy: str,
                 icon: int,
                 is_label_enable: int):
    
    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")
    if(row_size<1 or row_size>6):
        raise HTTPException(status_code=400, detail="row_size is illegal")
    if(column_size <1 or column_size>12 ):
        raise HTTPException(status_code=400, detail="column_size is illegal")
    
    connection, cursor = ConnectToDatabase()
    sql = f"INSERT INTO boards (`creator`, `tag`, `name`, `row_size`, `column_size`, `description`, `privacy`, `icon`, `is_label_enable`, `created_time`) \
            VALUES ('{creator}',{tag}, '{connection.escape_string(name)}', '{row_size}','{column_size}', '{connection.escape_string(description)}', '{connection.escape_string(privacy)}','{icon}','{is_label_enable}', now())"

    board_id = None
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        board_id = cursor.lastrowid
    
    finally:

        connection.close()
    
    if (board_id == None):

        raise HTTPException(status_code = 404)

    return DBUseIdGetBoard(board_id = board_id)

def DBEditBoard(board_id: int,
               tag: int,
               name: str,
               row_size: int,
               column_size: int,
               description: str,
               privacy: str,
               icon: int,
               is_label_enable: int):
    
    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")
    if(row_size<1 or row_size>6):
        raise HTTPException(status_code=400, detail="row_size is illegal")
    if(column_size <1 or column_size>12 ):
        raise HTTPException(status_code=400, detail="column_size is illegal")
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM boards \
            WHERE `id`={board_id}"
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
    sql = f"UPDATE boards \
            SET `tag`={tag}, \
                `name`='{connection.escape_string(name)}', \
                `row_size`='{row_size}', \
                `column_size`='{column_size}', \
                `description`='{connection.escape_string(description)}', \
                `privacy`='{connection.escape_string(privacy)}', \
                `icon`='{icon}', \
                `is_label_enable`='{is_label_enable}' \
            WHERE`id`={board_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return DBUseIdGetBoard(board_id = board_id)

def DBDeleteBoard(board_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM boards \
            WHERE `id`={board_id}"
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
    
    sql = f"DELETE FROM boards \
            WHERE `id`={board_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return 



if __name__ == "__main__":
    # print(DBUserSearchALLBoard(creator= 1,name= "")) #搜尋該使用者所有有權限看到的 images
    # print(DBShowUserAllBoard(creator= 1)) #顯示該使用者所有有權限看到的 images
    # print(DBShowAllUserCreateBoard(creator= 8))  #顯示該使用者創立的 images
    # print(DBSearchUserCreateBoard(creator=1 ,name= "keyboard")) #搜尋該使用者創立的 image
    # print(DBShowAllPublicBoard()) #顯示 public 的 images
    # print(DBSearchPublicBoard(name="o")) #搜尋 public 的 image
    # print(DBCreateBoard(creator= 1,tag = "NULL",name= "bannfatr",row_size= 2,column_size= 2,description= "for test",privacy= "private",icon = 2,is_label_enable= 1)) #新增board
    # print(DBEditBoard(board_id= 178,tag ="NULL",name= "b",row_size= 2,column_size= 2,description= "for test1",privacy= "private",icon= 2,is_label_enable= 1)) #編輯board
    # DBDeleteBoard(board_id= 183) #刪除board
    # print(DBUseIdGetBoard(board_id= 1)) #用id找board

    pass