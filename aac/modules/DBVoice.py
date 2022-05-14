import mariadb
from fastapi import HTTPException
from modules.ConnectToDatabase import ConnectToDatabase

def DBGetVoice(voice_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, privacy, location, created_time \
            FROM voices \
            WHERE `id`={voice_id}"
    voice = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, creator, privacy, location, created_time) in cursor:

            voice = {"id": id,
                     "creator": creator,
                     "privacy": privacy,
                     "location": location,
                     "created_time": created_time}
    finally:

        connection.close()

    if (voice == {}):

        raise HTTPException(status_code=404)

    return voice

def DBCreateVoice(creator: int,
                  privacy: str):

    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")
    location = "unknown"
    connection, cursor = ConnectToDatabase()
    sql = f"INSERT INTO voices (`creator`, `privacy`, `location`, `created_time`) \
            VALUES ('{creator}', '{connection.escape_string(privacy)}', '{connection.escape_string(location)}', now())"
    voice_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        voice_id = cursor.lastrowid  # 自增ID(尾部)

    finally:

        connection.close()

    if (voice_id == None):

        raise HTTPException(status_code=404)
    voice_location = str(voice_id) +".mp3"
    connection, cursor = ConnectToDatabase()
    sql = f"UPDATE voices \
            SET `location`='{connection.escape_string(voice_location)}' \
            WHERE `id`={voice_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBGetVoice(voice_id=voice_id)

def DBEditVoice(voice_id: id,
                privacy: str):

    if (privacy != "public" and privacy != "private"):
        raise HTTPException(status_code=400, detail="privacy is illegal")

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM voices \
            WHERE `id`={voice_id}"
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
    sql = f"UPDATE voices \
            SET privacy`='{connection.escape_string(privacy)}' \
            WHERE `id`={voice_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBGetVoice(voice_id=voice_id)

def DBDeleteVoice(voice_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM voices \
            WHERE `id`={voice_id}"
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
    sql = f"DELETE FROM voices \
            WHERE `id`={voice_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return

if __name__ == "__main__":
    #print(DBGetVoice(voice_id=161))
    #print(DBCreateVoice(creator= 1,privacy= "private"))
    #print(DBEditVoice(voice_id= 177, creator= 1,privacy= "private"))
    #try:
    DBDeleteVoice(voice_id = 176)
    #except print(0):
      #pass
