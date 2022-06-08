from fastapi import HTTPException
import mariadb
from modules.ConnectToDatabase import ConnectToDatabase


def DBShowAllEbookImages(ebook_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_images \
            WHERE `ebook_id`={ebook_id} " 
    ebooks_images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_image = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}
            ebooks_images.append(ebook_image)

    finally:

        connection.close()

    return ebooks_images

def DBSearchAllEbookImages(ebook_id: int,name:str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_images \
            WHERE name LIKE '%{connection.escape_string(name)}%'AND ebook_id={ebook_id}"
    ebooks_images = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_image = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}
            ebooks_images.append(ebook_image)

    finally:

        connection.close()
        
    return ebooks_images

def DBUseIdGetEbookImage(ebook_image_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_images \
            WHERE `id`={ebook_image_id}"
    ebook_image = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:
        
        print(sql)
        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_image = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}

    finally:

        connection.close()

    if (ebook_image == {}):

        raise HTTPException(status_code=404)

    return ebook_image

def DBCreateEbookImage(ebook_id: int,
                  name: str):
    
    connection, cursor = ConnectToDatabase()
    location = "unknown"
    sql = f"INSERT INTO ebooks_images (`ebook_id`, `name`,`location`,`created_time`) \
            VALUES ('{ebook_id}', '{connection.escape_string(name)}', '{connection.escape_string()}', '{connection.escape_string(location)}', now())"

    ebook_image_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        ebook_image_id = cursor.lastrowid  # 自增ID(尾部)
    finally:

        connection.close()

    if (ebook_image_id == None):

        raise HTTPException(status_code=404)
    
    connection, cursor = ConnectToDatabase()

    sql = f"UPDATE ebooks_images \
            SET `location`='{connection.escape_string(str(ebook_image_id))}' \
            WHERE `id`={ebook_image_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBUseIdGetEbookImage(ebook_image_id=ebook_image_id)

def DBEditEbookImage(ebook_image_id: int,
                name: str):
    
    connection, cursor = ConnectToDatabase()

    sql = f"SELECT id \
            FROM ebooks_images \
            WHERE `id`= {ebook_image_id}"
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

    sql = f"UPDATE ebooks_images \
            SET `name`='{connection.escape_string(name)}', \
                ``='{connection.escape_string()}' \
            WHERE `id`={ebook_image_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()
    return DBUseIdGetEbookImage(ebook_image_id=ebook_image_id)

def DBDeleteEbookImage(ebook_image_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_images \
            WHERE `id`={ebook_image_id}"
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
    sql = f"DELETE FROM ebooks_images \
            WHERE `id`={ebook_image_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return

if __name__ == "__main__":
     #print(DBCreateEbookImage(ebook_id=2, name="shouentesting3", ="public")) #創建ebook_image
     #print(DBEditEbookImage(ebook_image_id=203 , name="Google home",="private"))  #修改ebook_image
     #DBDeleteEbookImage(ebook_image_id=211) #刪除ebook_image
     #print(DBShowAllEbookImages(ebook_id=1))  #顯示該使用者所有有權限看到的 ebooks_images
     #print(DBSearchAllEbookImages(ebook_id=8,name="sh")) #搜尋該使用者所有有權限看到的 ebooks_images
     #print(DBUseIdGetEbookImage(ebook_image_id = 5555)) #用id找ebook_image
    pass