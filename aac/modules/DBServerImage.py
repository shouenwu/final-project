import mariadb
import time
from fastapi import HTTPException
from modules.ConnectToDatabase import ConnectToDatabase

def DBShowUserAllServerImages():
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, description, location, created_time \
            FROM server_images" 
    server_images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, name, description, location, created_time) in cursor:

            server_image = {"id": id,
                            "name": name,
                            "description": description,
                            "location": location,
                            "created_time": created_time}
            server_images.append(server_image)

    finally:

        connection.close()

    return server_images

def DBSearchAllServerImages(name: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, description, location, created_time \
            FROM server_images \
            WHERE name LIKE '%{connection.escape_string(name)}%'"
    server_images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, name, description, location, created_time) in cursor:

            server_image = {"id": id,
                            "name": name,
                            "description": description,
                            "location": location,
                            "created_time": created_time}
            server_images.append(server_image)

    finally:

        connection.close()
        
    return server_images

def DBUseIdGetServerImage(server_image_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, description, location, created_time \
            FROM server_images \
            WHERE `id`={server_image_id}"
    server_image = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, name, description, location, created_time) in cursor:

            server_image = {"id": id,
                            "name": name,
                            "description": description,
                            "location": location,
                            "created_time": created_time}

    finally:

        connection.close()

    if (server_image == {}):

        raise HTTPException(status_code=404)

    return server_image

def DBCreateServerImage(name: str,
                        description: str):
    
    connection, cursor = ConnectToDatabase()
    location = "unknown"
    if(description == ""):

        sql = f"INSERT INTO server_images (`name`, `description`, `location`,`created_time`) \
                VALUES ('{connection.escape_string(name)}', NULL , '{connection.escape_string(location)}', now())"
    else:

        sql = f"INSERT INTO server_images (`name`, `description`, `location`,`created_time`) \
                VALUES ('{connection.escape_string(name)}', '{connection.escape_string(description)}', '{connection.escape_string(location)}', now())"
    server_image_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        server_image_id = cursor.lastrowid  # 自增ID(尾部)
    finally:

        connection.close()

    if (server_image_id == None):

        raise HTTPException(status_code=404)
    
    connection, cursor = ConnectToDatabase()

    sql = f"UPDATE server_images \
            SET `location`='{connection.escape_string(str(server_image_id))}' \
            WHERE `id`={server_image_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBUseIdGetServerImage(server_image_id=server_image_id)

def DBEditServerImage(server_image_id: int,
                name: str,
                description: str):
    
    connection, cursor = ConnectToDatabase()

    sql = f"SELECT id \
            FROM server_images \
            WHERE `id`= {server_image_id}"
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

        sql = f"UPDATE server_images \
                SET `name`='{connection.escape_string(name)}', \
                    `description`= NULL \
                WHERE `id`={server_image_id}"
    else:

        sql = f"UPDATE server_images \
                SET `name`='{connection.escape_string(name)}', \
                    `description`='{connection.escape_string(description)}' \
                WHERE `id`={server_image_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()
    return DBUseIdGetServerImage(server_image_id=server_image_id)

def DBDeleteServerImage(server_image_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM server_images \
            WHERE `id`={server_image_id}"
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
    sql = f"DELETE FROM server_images \
            WHERE `id`={server_image_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return

if __name__ == "__main__":
     #print(DBCreateServerImage(name="shouentesting", description="abc123")) #創建 server_image
     print(DBEditServerImage(server_image_id=6 , name="Google home",description=""))  #修改 server_image
     #DBDeleteServerImage(server_image_id=4) #刪除 server_image
     #print(DBShowUserAllServerImages())  #顯示所有的 server_images
     #print(DBSearchAllServerImages(name="nc")) #以名字搜尋所有關聯的 server_images
     #print(DBUseIdGetServerImage(server_image_id = 1)) #用id找 server_image