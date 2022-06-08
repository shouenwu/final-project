from fastapi import HTTPException
import mariadb
from modules.ConnectToDatabase import ConnectToDatabase

def DBUserSearchALLEbook(creator: int,
                    title: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time \
            FROM ebooks \
            WHERE title LIKE '%{connection.escape_string(title)}%'AND (creator={creator} OR privacy = 'public')"
    ebooks = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time) in cursor:

            ebook = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "title": title,
                    "page_num": page_num,
                    "description": description,
                    "privacy": privacy,
                    "cover_image_location": cover_image_location,
                    "created_time": created_time}
            ebooks.append(ebook)

    finally:

        connection.close()

    return ebooks

def DBShowUserAllEbook(creator: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time \
            FROM ebooks \
            WHERE creator={creator} OR privacy = 'public'"
    ebooks = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, title, page_num, description, privacy, cover_image_location , created_time) in cursor:

            ebook = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "title": title,
                    "page_num": page_num,
                    "description": description,
                    "privacy": privacy,
                    "cover_image_location": cover_image_location,
                    "created_time": created_time}
            ebooks.append(ebook)

    finally:

        connection.close()

    return ebooks

def DBShowAllUserCreateEbook(creator: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time \
            FROM ebooks \
            WHERE creator={creator}"
    ebooks = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time) in cursor:

            ebook = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "title": title,
                    "page_num": page_num,
                    "description": description,
                    "privacy": privacy,
                    "cover_image_location": cover_image_location,
                    "created_time": created_time}
            ebooks.append(ebook)

    finally:

        connection.close()
    return ebooks

def DBShowAllPublicEbook():
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time \
            FROM ebooks \
            WHERE privacy= 'public'"
    ebooks = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time) in cursor:

            ebook = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "title": title,
                    "page_num": page_num,
                    "description": description,
                    "privacy": privacy,
                    "cover_image_location": cover_image_location,
                    "created_time": created_time}
            ebooks.append(ebook)

    finally:

        connection.close()
    return ebooks

def DBSearchPublicEbook(title: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time \
            FROM ebooks \
            WHERE privacy= 'public' AND title LIKE '%{connection.escape_string(title)}%'"
    ebooks = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, title,  page_num, description, privacy, cover_image_location , created_time) in cursor:

            ebook = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "title": title,
                    "page_num": page_num,
                    "description": description,
                    "privacy": privacy,
                    "cover_image_location": cover_image_location,
                    "created_time": created_time}
            ebooks.append(ebook)

    finally:

        connection.close()
    return ebooks

def DBSearchUserCreateEbook(creator: int,
                        title: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time \
            FROM ebooks \
            WHERE `creator`={creator} AND title LIKE '%{connection.escape_string(title)}%'"
    ebooks = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time) in cursor:

            ebook = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "title": title,
                    "page_num": page_num,
                    "description": description,
                    "privacy": privacy,
                    "cover_image_location": cover_image_location,
                    "created_time": created_time}
            ebooks.append(ebook)

    finally:

        connection.close()
    return ebooks

def DBUseIdGetEbook(ebook_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, tag, title,  page_num, description, privacy, cover_image_location , created_time \
            FROM ebooks \
            WHERE id = {ebook_id}"
    ebook = {}

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, tag, title , page_num, description, privacy, cover_image_location , created_time) in cursor:

            ebook = {"id": id,
                    "creator": creator,
                    "tag": tag,
                    "title": title,
                    "page_num": page_num,
                    "description": description,
                    "privacy": privacy,
                    "cover_image_location": cover_image_location,
                    "created_time": created_time}

    finally:

        connection.close()

    if (ebook =={}):

        raise HTTPException(status_code = 404)

    return ebook

def DBCreateEbook(creator: int,
                 tag: int,
                 title: str,
                 page_num: int,
                 description: str,
                 privacy: str):
    
    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")
    
    connection, cursor = ConnectToDatabase()
    cover_image_location = "unknown"
    sql = f"INSERT INTO ebooks (`creator`, `tag`, `title`, `page_num`, `description`, `privacy`, `cover_image_location`, `created_time`) \
            VALUES ('{creator}',{tag}, '{connection.escape_string(title)}','{page_num}', '{connection.escape_string(description)}', '{connection.escape_string(privacy)}','{connection.escape_string(cover_image_location)}', now())"

    ebook_id = None
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        ebook_id = cursor.lastrowid
    
    finally:

        connection.close()
    
    if (ebook_id == None):

        raise HTTPException(status_code = 404)
    
    connection, cursor = ConnectToDatabase()

    sql = f"UPDATE ebooks \
            SET `cover_image_location`='{connection.escape_string(str(ebook_id))}' \
            WHERE `id`={ebook_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBUseIdGetEbook(ebook_id = ebook_id)

def DBEditEbook(ebook_id: int,
               tag: int,
               title: str,
               page_num: int,
               description: str,
               privacy: str):
    
    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks \
            WHERE `id`={ebook_id}"
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
    sql = f"UPDATE ebooks \
            SET `tag`={tag}, \
                `title`='{connection.escape_string(title)}', \
                `page_num`='{page_num}', \
                `description`='{connection.escape_string(description)}', \
                `privacy`='{connection.escape_string(privacy)}' \
            WHERE`id`={ebook_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return DBUseIdGetEbook(ebook_id = ebook_id)

def DBDeleteEbook(ebook_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks \
            WHERE `id`={ebook_id}"
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
    
    sql = f"DELETE FROM ebooks \
            WHERE `id`={ebook_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return 



if __name__ == "__main__":
    #print(DBUserSearchALLEbook(creator= 1,title= "")) #搜尋該使用者所有有權限看到的 ebooks success
    #print(DBShowUserAllEbook(creator= 2)) #顯示該使用者所有有權限看到的 ebooks success
    #print(DBShowAllUserCreateEbook(creator= 1))  #顯示該使用者創立的 ebooks success
    #print(DBSearchUserCreateEbook(creator=1 ,title= "b")) #搜尋該使用者創立的 ebook success
    #print(DBShowAllPublicEbook()) #顯示 public 的 ebooks success
    #print(DBSearchPublicEbook(title="o")) #搜尋 public 的 ebook
    #DBCreateEbook(creator= 8,tag = "NULL",title= "front_test4",page_num= 2,description= "for test",privacy= "public") #新增ebook success
    #DBEditEbook(ebook_id= 1,tag ="NULL",title= "b",page_num= 2,description= "modify for test1",privacy= "public")#編輯ebook success
    #DBDeleteEbook(ebook_id= 1) #刪除ebook success
    #print(DBUseIdGetEbook(ebook_id= 2)) #用id找ebook success
    pass