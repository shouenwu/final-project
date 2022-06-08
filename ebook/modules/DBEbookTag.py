import mariadb
from fastapi import HTTPException
from modules.ConnectToDatabase import ConnectToDatabase

def DBUserSearchEbookTag(creator: int,
                         name: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, description, created_time \
            FROM ebook_tags \
            WHERE name LIKE '%{connection.escape_string(name)}%' AND creator ={creator}"
    ebook_tags = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, name, description, created_time) in cursor:

            ebook_tag = {"id": id,
                    "creator": creator,
                    "name": name,
                    "description": description,
                    "created_time": created_time}
            ebook_tags.append(ebook_tag)

    finally:

        connection.close()

    return ebook_tags

def DBShowAllUserEbookTag(creator: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, description, created_time \
            FROM ebook_tags \
            WHERE creator ={creator}"
    ebook_tags = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator, name, description, created_time) in cursor:

            ebook_tag = {"id": id,
                    "creator": creator,
                    "name": name,
                    "description": description,
                    "created_time": created_time}
            ebook_tags.append(ebook_tag)

    finally:

        connection.close()

    return ebook_tags

def DBGetEbookTag(ebook_tag_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, creator, name, description, created_time \
            FROM ebook_tags \
            WHERE `id`={ebook_tag_id}"
    ebook_tag = {}

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, creator,  name,  description, created_time) in cursor:

            ebook_tag = {"id": id,
                    "creator": creator,
                    "name": name,
                    "description": description,
                    "created_time": created_time}

    finally:

        connection.close()

    if (ebook_tag =={}):

        raise HTTPException(status_code = 404)

    return ebook_tag

def DBCreateEbookTag(creator: int,
                   name: str,
                   description: str):

    connection, cursor = ConnectToDatabase()
    sql = f"INSERT INTO ebook_tags (`creator`, `name`, `description`, `created_time`) \
            VALUES ('{creator}', '{connection.escape_string(name)}', '{connection.escape_string(description)}', now())"

    ebook_tag_id = None
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        ebook_tag_id = cursor.lastrowid
    
    finally:

        connection.close()
    
    if (ebook_tag_id == None):

        raise HTTPException(status_code = 404)

    return DBGetEbookTag(ebook_tag_id = ebook_tag_id)

def DBEditEbookTag(ebook_tag_id: int,
                  name: str,
                  description: str):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebook_tags \
            WHERE `id`={ebook_tag_id}"
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
    sql = f"UPDATE ebook_tags \
            SET `name`='{connection.escape_string(name)}', \
                `description`='{connection.escape_string(description)}' \
            WHERE`id`={ebook_tag_id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return DBGetEbookTag(ebook_tag_id = ebook_tag_id)

def DBDeleteEbookTag(ebook_tag_id: int):
    
    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebook_tags \
            WHERE `id`={ebook_tag_id}"
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
    
    sql = f"DELETE FROM ebook_tags \
            WHERE `id`={ebook_tag_id}"
    
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
    #print(DBUserSearchEbookTag(creator = 1,name = "b"))
    #print(DBShowAllUserEbookTag(creator = 1))
    #print(DBGetEbookTag(ebook_tag_id= 16))
    #print(DBCreateEbookTag(creator= 1,name= "testing",description= "for test"))
    #print(DBEditEbookTag(ebook_tag_id= 18,name= "b",description= "for test"))
    #DBDeleteEbookTag(ebook_tag_id= 16)