import mariadb
from fastapi import HTTPException
from modules.ConnectToDatabase import ConnectToDatabase

def DBShowAllEbookPages(ebook_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM ebooks_pages\
            WHERE `ebook_id`={ebook_id}"
    ebooks_pages = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    else:

        for (id, ebook_id, page_no, column_index, subtitle, text_color, text_background_color, content) in cursor:

            page = {"id": id,
                      "ebook_id": ebook_id,
                      "page_no": page_no,
                      "column_index": column_index,
                      "subtitle": subtitle,
                      "text_color": text_color,
                      "text_background_color": text_background_color,
                      "content": content,
                      }
            ebooks_pages.append(page)

    finally:

        connection.close()

    return ebooks_pages


def DBSearchPageInEbook(ebook_id: int, ebook_subtitle: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM ebooks_pages\
            WHERE `ebook_id`={ebook_id} AND `subtitle` LIKE '%{connection.escape_string(ebook_subtitle)}%'"
    ebooks_pages = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    else:

        for (id, ebook_id, page_no, column_index, subtitle, text_color, text_background_color, content) in cursor:

            page = {"id": id,
                      "ebook_id": ebook_id,
                      "page_no": page_no,
                      "column_index": column_index,
                      "subtitle": subtitle,
                      "text_color": text_color,
                      "text_background_color": text_background_color,
                      "content": content,
                    }
            ebooks_pages.append(page)

    finally:

        connection.close()

    return ebooks_pages


def DBGetEbookPage(page_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM ebooks_pages \
            WHERE `id`={page_id}"
    page = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    else:

        for (id, ebook_id, page_no, column_index, subtitle,text_color, text_background_color, content) in cursor:

            page = {"id": id,
                      "ebook_id": ebook_id,
                      "page_no": page_no,
                      "column_index": column_index,
                      "subtitle": subtitle,
                      "text_color": text_color,
                      "text_background_color": text_background_color,
                      "content": content,
                    }

    finally:

        connection.close()

    if (page == {}):

        raise HTTPException(_code=404)

    return page


def DBCreatePage(ebook_id: int,
                   page_no: int,
                   column_index: int,
                   subtitle: str,
                   text_color: str,
                   text_background_color: str,
                   content: str):

    connection, cursor = ConnectToDatabase()
    if (content ==""):
        
        sql = f"INSERT INTO ebooks_pages ( `ebook_id`,`page_no`,`column_index`,`subtitle`,``,`text_color`,`text_background_color`,`content`) \
                VALUES ( '{ebook_id}', '{page_no}','{column_index}', '{connection.escape_string(subtitle)}', '{connection.escape_string()}', '{connection.escape_string(text_color)}', '{connection.escape_string(text_background_color)}', NULL)"
    else:
        
        sql = f"INSERT INTO ebooks_pages ( `ebook_id`,`page_no`,`column_index`,`subtitle`,``,`text_color`,`text_background_color,`content`) \
                VALUES ( '{ebook_id}', '{page_no}','{column_index}', '{connection.escape_string(subtitle)}', '{connection.escape_string()}', '{connection.escape_string(text_color)}', '{connection.escape_string(text_background_color)}', '{connection.escape_string(content)}')"
    page_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    else:

        page_id = cursor.lastrowid

    finally:

        connection.close()

    if (page_id == None):

        raise HTTPException(_code=404)

    return DBGetEbookPage(page_id=page_id)


def DBEditPage(page_id: int,
                 subtitle: str,
                 text_color: str,
                 text_background_color: str,
                 content: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_pages \
            WHERE `id`={page_id}"
    whether_id_exist = False

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    else:

        for (id) in cursor:

            whether_id_exist = True

    finally:

        connection.close()
    if (whether_id_exist == False):

        raise HTTPException(_code=404, detail="page_id doesn't exist")
    
    connection, cursor = ConnectToDatabase()
    if (content ==""):
       
        sql = f"UPDATE ebooks_pages \
                SET `subtitle`='{connection.escape_string(subtitle)}', \
                    ``='{connection.escape_string()}' ,\
                    `text_color`='{connection.escape_string(text_color)}', \
                    `text_background_color`='{connection.escape_string(text_background_color)}', \
                    `content`= NULL\
                WHERE`id`={page_id}"
    else:
        
        sql = f"UPDATE ebooks_pages \
                SET `subtitle`='{connection.escape_string(subtitle)}', \
                    ``='{connection.escape_string()}' ,\
                    `text_color`='{connection.escape_string(text_color)}', \
                    `text_background_color`='{connection.escape_string(text_background_color)}', \
                    `content`='{connection.escape_string(content)}'\
                WHERE`id`={page_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    finally:

        connection.close()
    
    return DBGetEbookPage(page_id=page_id)


def DBClearPage(page_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM ebooks_pages \
            WHERE `id`={page_id}"
    whether_id_exist = False

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    else:

        for (id) in cursor:

            whether_id_exist = True

    finally:

        connection.close()
    if (whether_id_exist == False):

        raise HTTPException(_code=404, detail="page_id doesn't exist")
    
    text_color="#000000"
    text_background_color="#FFFFFF"

    connection, cursor = ConnectToDatabase()
    sql = f"UPDATE ebooks_pages \
            SET `subtitle`='', \
                ``='{connection.escape_string()}' ,\
                `text_color`='{connection.escape_string(text_color)}', \
                `text_background_color`='{connection.escape_string(text_background_color)}', \
                `content`= NULL \
            WHERE`id`={page_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(_code=500)

    finally:

        connection.close()

    return DBGetEbookPage(page_id=page_id)


if __name__ == "__main__":

    #print(DBGetEbookPage(page_id= 1936))
    # print(DBShowAllEbookPages(ebook_id = 43))
    # print(DBSearchPageInEbook(ebook_id=43, ebook_subtitle="123"))
    # print(DBCreateEbookPage(ebook_id=43,
    # page_no=0,
    # column_index=0,
    #subtitle="new page",
    # ="#000000",
    # text_color="#000000",
    # text_background_color="#FFFFFF",
    # =0,
    # ="NULL",
    # =1,
    # ="NULL",
    # content="",
    # =0,
    # =0))
    # print(DBEditEbookPage(page_id =1283,
    # subtitle="null",
    # ="#000000",
    # text_color="#000000",
    # text_background_color="#FFFFFF",
    # =0,
    # ="NULL",
    # =1,
    # ="NULL",
    # content="",
    # =0,
    # =0))
    # DBClearEbookPage(page_id=1347)
    pass
