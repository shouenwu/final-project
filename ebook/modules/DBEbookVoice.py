from fastapi import HTTPException
import mariadb
from modules.ConnectToDatabase import ConnectToDatabase


def DBShowAllEbookVoices(ebook_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_voices \
            WHERE `ebook_id`={ebook_id} " 
    ebooks_voices = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_voice = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}
            ebooks_voices.append(ebook_voice)

    finally:

        connection.close()

    return ebooks_voices

def DBSearchAllEbookVoices(ebook_id: int,name:str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_voices \
            WHERE name LIKE '%{connection.escape_string(name)}%'AND ebook_id={ebook_id}"
    ebooks_voices = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_voice = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}
            ebooks_voices.append(ebook_voice)

    finally:

        connection.close()
        
    return ebooks_voices

def DBUseIdGetEbookVoice(ebook_voice_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_voices \
            WHERE `id`={ebook_voice_id}"
    ebook_voice = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:
        
        print(sql)
        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_voice = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}

    finally:

        connection.close()

    if (ebook_voice == {}):

        raise HTTPException(status_code=404)

    return ebook_voice

def DBCreateEbookVoice(ebook_id: int,
                  name: str):
    
    connection, cursor = ConnectToDatabase()
    location = "unknown"
    sql = f"INSERT INTO ebooks_voices (`ebook_id`, `name`,`location`,`created_time`) \
            VALUES ('{ebook_id}', '{connection.escape_string(name)}', '{connection.escape_string()}', '{connection.escape_string(location)}', now())"

    ebook_voice_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        ebook_voice_id = cursor.lastrowid  # 自增ID(尾部)
    finally:

        connection.close()

    if (ebook_voice_id == None):

        raise HTTPException(status_code=404)
    
    connection, cursor = ConnectToDatabase()

    sql = f"UPDATE ebooks_voices \
            SET `location`='{connection.escape_string(str(ebook_voice_id))}' \
            WHERE `id`={ebook_voice_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBUseIdGetEbookVoice(ebook_voice_id=ebook_voice_id)

def DBEditEbookVoice(ebook_voice_id: int,
                name: str):
    
    connection, cursor = ConnectToDatabase()

    sql = f"SELECT id \
            FROM ebooks_voices \
            WHERE `id`= {ebook_voice_id}"
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

    sql = f"UPDATE ebooks_voices \
            SET `name`='{connection.escape_string(name)}', \
                ``='{connection.escape_string()}' \
            WHERE `id`={ebook_voice_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()
    return DBUseIdGetEbookVoice(ebook_voice_id=ebook_voice_id)

def DBDeleteEbookVoice(ebook_voice_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_voices \
            WHERE `id`={ebook_voice_id}"
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
    sql = f"DELETE FROM ebooks_voices \
            WHERE `id`={ebook_voice_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return

if __name__ == "__main__":
     #print(DBCreateEbookVoice(ebook_id=2, name="shouentesting3", ="public")) #創建ebook_voice
     #print(DBEditEbookVoice(ebook_voice_id=203 , name="Google home",="private"))  #修改ebook_voice
     #DBDeleteEbookVoice(ebook_voice_id=211) #刪除ebook_voice
     #print(DBShowAllEbookVoices(ebook_id=1))  #顯示該使用者所有有權限看到的 ebooks_voices
     #print(DBSearchAllEbookVoices(ebook_id=8,name="sh")) #搜尋該使用者所有有權限看到的 ebooks_voices
     #print(DBUseIdGetEbookVoice(ebook_voice_id = 5555)) #用id找ebook_voice
    pass