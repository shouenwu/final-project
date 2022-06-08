from fastapi import HTTPException
import mariadb
from modules.ConnectToDatabase import ConnectToDatabase


def DBShowAllEbookTexts(ebook_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, content, created_time \
            FROM ebooks_texts \
            WHERE `ebook_id`={ebook_id} " 
    ebooks_texts = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, content, created_time) in cursor:

            ebook_text = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "content": content,
                     "created_time": created_time}
            ebooks_texts.append(ebook_text)

    finally:

        connection.close()

    return ebooks_texts

def DBSearchAllEbookTexts(ebook_id: int,name:str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, content, created_time \
            FROM ebooks_texts \
            WHERE name LIKE '%{connection.escape_string(name)}%'AND ebook_id={ebook_id}"
    ebooks_texts = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, content, created_time) in cursor:

            ebook_text = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "content": content,
                     "created_time": created_time}
            ebooks_texts.append(ebook_text)

    finally:

        connection.close()
        
    return ebooks_texts

def DBUseIdGetEbookText(ebook_text_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, content, created_time \
            FROM ebooks_texts \
            WHERE `id`={ebook_text_id}"
    ebook_text = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:
        
        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, content, created_time) in cursor:

            ebook_text = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "content": content,
                     "created_time": created_time}

    finally:

        connection.close()

    if (ebook_text == {}):

        raise HTTPException(status_code=404)

    return ebook_text

def DBCreateEbookText(ebook_id: int,
                  name: str):
    
    connection, cursor = ConnectToDatabase()
    content = "unknown"
    sql = f"INSERT INTO ebooks_texts (`ebook_id`, `name`,`content`,`created_time`) \
            VALUES ('{ebook_id}', '{connection.escape_string(name)}', '{connection.escape_string()}', '{connection.escape_string(content)}', now())"

    ebook_text_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        ebook_text_id = cursor.lastrowid  # 自增ID(尾部)
    finally:

        connection.close()

    if (ebook_text_id == None):

        raise HTTPException(status_code=404)
    
    connection, cursor = ConnectToDatabase()

    sql = f"UPDATE ebooks_texts \
            SET `content`='{connection.escape_string(str(ebook_text_id))}' \
            WHERE `id`={ebook_text_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBUseIdGetEbookText(ebook_text_id=ebook_text_id)

def DBEditEbookText(ebook_text_id: int,
                name: str,
                content: str):
    
    connection, cursor = ConnectToDatabase()

    sql = f"SELECT id \
            FROM ebooks_texts \
            WHERE `id`= {ebook_text_id}"
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

    sql = f"UPDATE ebooks_texts \
            SET `name`='{connection.escape_string(name)}', \
                `content`='{connection.escape_string(content)}' \
            WHERE `id`={ebook_text_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()
    return DBUseIdGetEbookText(ebook_text_id=ebook_text_id)

def DBDeleteEbookText(ebook_text_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_texts \
            WHERE `id`={ebook_text_id}"
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
    sql = f"DELETE FROM ebooks_texts \
            WHERE `id`={ebook_text_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return

if __name__ == "__main__":
     #print(DBCreateEbookText(ebook_id=2, name="shouentesting3", ="public")) #創建ebook_text
     #print(DBEditEbookText(ebook_text_id=203 , name="Google home",="private"))  #修改ebook_text
     #DBDeleteEbookText(ebook_text_id=211) #刪除ebook_text
     #print(DBShowAllEbookTexts(ebook_id=1))  #顯示該使用者所有有權限看到的 ebooks_texts
     #print(DBSearchAllEbookTexts(ebook_id=8,name="sh")) #搜尋該使用者所有有權限看到的 ebooks_texts
     #print(DBUseIdGetEbookText(ebook_text_id = 5555)) #用id找ebook_text
    pass