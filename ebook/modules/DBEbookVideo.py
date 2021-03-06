from fastapi import HTTPException
import mariadb
from modules.ConnectToDatabase import ConnectToDatabase


def DBShowAllEbookVideos(ebook_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_videos \
            WHERE `ebook_id`={ebook_id} " 
    ebooks_videos = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_video = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}
            ebooks_videos.append(ebook_video)

    finally:

        connection.close()

    return ebooks_videos

def DBSearchAllEbookVideos(ebook_id: int,name:str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_videos \
            WHERE name LIKE '%{connection.escape_string(name)}%'AND ebook_id={ebook_id}"
    ebooks_videos = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_video = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}
            ebooks_videos.append(ebook_video)

    finally:

        connection.close()
        
    return ebooks_videos

def DBUseIdGetEbookVideo(ebook_video_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, ebook_id, name, location, created_time \
            FROM ebooks_videos \
            WHERE `id`={ebook_video_id}"
    ebook_video = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:
        
        print(sql)
        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, ebook_id, name, location, created_time) in cursor:

            ebook_video = {"id": id,
                     "ebook_id": ebook_id,
                     "name": name,
                     "location": location,
                     "created_time": created_time}

    finally:

        connection.close()

    if (ebook_video == {}):

        raise HTTPException(status_code=404)

    return ebook_video

def DBCreateEbookVideo(ebook_id: int,
                  name: str):
    
    connection, cursor = ConnectToDatabase()
    location = "unknown"
    sql = f"INSERT INTO ebooks_videos (`ebook_id`, `name`,`location`,`created_time`) \
            VALUES ('{ebook_id}', '{connection.escape_string(name)}', '{connection.escape_string()}', '{connection.escape_string(location)}', now())"

    ebook_video_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        ebook_video_id = cursor.lastrowid  # ??????ID(??????)
    finally:

        connection.close()

    if (ebook_video_id == None):

        raise HTTPException(status_code=404)
    
    connection, cursor = ConnectToDatabase()

    sql = f"UPDATE ebooks_videos \
            SET `location`='{connection.escape_string(str(ebook_video_id))}' \
            WHERE `id`={ebook_video_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBUseIdGetEbookVideo(ebook_video_id=ebook_video_id)

def DBEditEbookVideo(ebook_video_id: int,
                name: str):
    
    connection, cursor = ConnectToDatabase()

    sql = f"SELECT id \
            FROM ebooks_videos \
            WHERE `id`= {ebook_video_id}"
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

    sql = f"UPDATE ebooks_videos \
            SET `name`='{connection.escape_string(name)}', \
                ``='{connection.escape_string()}' \
            WHERE `id`={ebook_video_id}"
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()
    return DBUseIdGetEbookVideo(ebook_video_id=ebook_video_id)

def DBDeleteEbookVideo(ebook_video_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_videos \
            WHERE `id`={ebook_video_id}"
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
    sql = f"DELETE FROM ebooks_videos \
            WHERE `id`={ebook_video_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return

if __name__ == "__main__":
     #print(DBCreateEbookVideo(ebook_id=2, name="shouentesting3", ="public")) #??????ebook_video
     #print(DBEditEbookVideo(ebook_video_id=203 , name="Google home",="private"))  #??????ebook_video
     #DBDeleteEbookVideo(ebook_video_id=211) #??????ebook_video
     #print(DBShowAllEbookVideos(ebook_id=1))  #?????????????????????????????????????????? ebooks_videos
     #print(DBSearchAllEbookVideos(ebook_id=8,name="sh")) #?????????????????????????????????????????? ebooks_videos
     #print(DBUseIdGetEbookVideo(ebook_video_id = 5555)) #???id???ebook_video
    pass