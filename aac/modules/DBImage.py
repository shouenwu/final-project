from fastapi import HTTPException



import mariadb


from modules.ConnectToDatabase import ConnectToDatabase



def DBShowUserCreateImages(creator: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, privacy, location, created_time \
            FROM images \
            WHERE `creator`={creator}"
    images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, name, privacy, location, created_time) in cursor:

            image = {"id": id,
                     "creator": creator,
                     "name": name,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}
            images.append(image)

    finally:

        connection.close()

    return images

def DBSearchUserCreateImages(creator: int,name: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, privacy, location, created_time \
            FROM images \
            WHERE creator= {creator} AND name LIKE '%{connection.escape_string(name)}%'"
    images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, name, privacy, location, created_time) in cursor:

            image = {"id": id,
                     "creator": creator,
                     "name": name,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}
            images.append(image)

    finally:

        connection.close()

    return images

def DBShowPublicImages():

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, privacy, location, created_time \
            FROM images \
            WHERE `privacy`='public' "
    images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, name, privacy, location, created_time) in cursor:

            image = {"id": id,
                     "creator": creator,
                     "name": name,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}
            images.append(image)

    finally:

        connection.close()

    return images

def DBSearchPublicImages(name: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, privacy, location, created_time \
            FROM images \
            WHERE privacy= 'public' AND name LIKE '%{connection.escape_string(name)}%'"
    images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, name, privacy, location, created_time) in cursor:

            image = {"id": id,
                     "creator": creator,
                     "name": name,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}
            images.append(image)

    finally:

        connection.close()

    return images

def DBShowUserAllImages(creator: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, privacy, location, created_time \
            FROM images \
            WHERE `creator`={creator} OR `privacy`='public'" 
    images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, name, privacy, location, created_time) in cursor:

            image = {"id": id,
                     "creator": creator,
                     "name": name,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}
            images.append(image)

    finally:

        connection.close()

    return images

def DBSearchUserAllImages(creator: int,name:str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, privacy, location, created_time \
            FROM images \
            WHERE name LIKE '%{connection.escape_string(name)}%'AND (creator={creator} OR privacy = 'public')"
    images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, name, privacy, location, created_time) in cursor:

            image = {"id": id,
                     "creator": creator,
                     "name": name,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}
            images.append(image)

    finally:

        connection.close()
        
    return images

def DBUseIdGetImage(image_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, privacy, location, created_time \
            FROM images \
            WHERE `id`={image_id}"
    image = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:
        
        print(sql)
        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, name, privacy, location, created_time) in cursor:

            image = {"id": id,
                     "creator": creator,
                     "name": name,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}

    finally:

        connection.close()

    if (image == {}):

        raise HTTPException(status_code=404)

    return image

def DBCreateImage(creator: int,
                  name: str,
                  privacy: str):

    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")
    
    
    connection, cursor = ConnectToDatabase()
    location = "unknown"
    sql = f"INSERT INTO images (`creator`, `name`, `privacy`, `location`,`created_time`) \
            VALUES ('{creator}', '{connection.escape_string(name)}', '{connection.escape_string(privacy)}', '{connection.escape_string(location)}', now())"

    image_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        image_id = cursor.lastrowid  # ??????ID(??????)
    finally:

        connection.close()

    if (image_id == None):

        raise HTTPException(status_code=404)
    
    connection, cursor = ConnectToDatabase()

    sql = f"UPDATE images \
            SET `location`='{connection.escape_string(str(image_id))}' \
            WHERE `id`={image_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBUseIdGetImage(image_id=image_id)

def DBEditImage(image_id: int,
                name: str,
                privacy: str):

    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")
    
    connection, cursor = ConnectToDatabase()

    sql = f"SELECT id \
            FROM images \
            WHERE `id`= {image_id}"
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

    sql = f"UPDATE images \
            SET `name`='{connection.escape_string(name)}', \
                `privacy`='{connection.escape_string(privacy)}' \
            WHERE `id`={image_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()
    return DBUseIdGetImage(image_id=image_id)

def DBDeleteImage(image_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM images \
            WHERE `id`={image_id}"
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
    sql = f"DELETE FROM images \
            WHERE `id`={image_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return

if __name__ == "__main__":
     
     #print(DBCreateImage(creator=2, name="shouentesting3", privacy="public")) #??????image
     #print(DBEditImage(image_id=203 , name="Google home",privacy="private"))  #??????image
     #DBDeleteImage(image_id=211) #??????image
     #print(DBShowPublicImages()) #??????public images
     #print(DBSearchPublicImages(name="sh")) #??????public image
     #print(DBShowUserCreateImages(creator =1)) #??????????????????????????? images
     #print(DBSearchUserCreateImages(creator = 8,name ="Google")) #??????????????????????????? images
     #print(DBShowUserAllImages(creator=1))  #?????????????????????????????????????????? images
     #print(DBSearchUserAllImages(creator=8,name="sh")) #?????????????????????????????????????????? images
     #print(DBUseIdGetImage(image_id = 5555)) #???id???image
    pass