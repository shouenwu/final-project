import mariadb
from fastapi import HTTPException

from modules.ConnectToDatabase import ConnectToDatabase

def DBShowAllBoardButtons(board_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM buttons\
            WHERE `board`={board_id}"
    buttons = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, board, row_index, column_index, label, label_color, name_color, background_color, category, image, is_image_enable, voice, hyperlink, is_hyperlink_inside, status) in cursor:

            button = {"id": id,
                      "board": board,
                      "row_index": row_index,
                      "column_index": column_index,
                      "label": label,
                      "label_color": label_color,
                      "name_color": name_color,
                      "background_color": background_color,
                      "category": category,
                      "image": image,
                      "is_image_enable": is_image_enable,
                      "voice": voice,
                      "hyperlink": hyperlink,
                      "is_hyperlink_inside": is_hyperlink_inside,
                      "status": status}
            buttons.append(button)

    finally:

        connection.close()

    return buttons

def DBSearchButtonInBoard(board_id: int, board_label: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM buttons\
            WHERE `board`={board_id} AND `label` LIKE '%{connection.escape_string(board_label)}%'"
    buttons = []

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, board, row_index, column_index, label, label_color, name_color, background_color, category, image, is_image_enable, voice, hyperlink, is_hyperlink_inside, status) in cursor:

            button = {"id": id,
                      "board": board,
                      "row_index": row_index,
                      "column_index": column_index,
                      "label": label,
                      "label_color": label_color,
                      "name_color": name_color,
                      "background_color": background_color,
                      "category": category,
                      "image": image,
                      "is_image_enable": is_image_enable,
                      "voice": voice,
                      "hyperlink": hyperlink,
                      "is_hyperlink_inside": is_hyperlink_inside,
                      "status": status}
            buttons.append(button)

    finally:

        connection.close()

    return buttons

def DBGetButton(button_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT * \
            FROM buttons \
            WHERE `id`={button_id}"
    button = {}

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        for (id, board, row_index, column_index, label, label_color, name_color, background_color, category, image, is_image_enable, voice, hyperlink, is_hyperlink_inside, status) in cursor:

            button = {"id": id,
                      "board": board,
                      "row_index": row_index,
                      "column_index": column_index,
                      "label": label,
                      "label_color": label_color,
                      "name_color": name_color,
                      "background_color": background_color,
                      "category": category,
                      "image": image,
                      "is_image_enable": is_image_enable,
                      "voice": voice,
                      "hyperlink": hyperlink,
                      "is_hyperlink_inside": is_hyperlink_inside,
                      "status": status}

    finally:

        connection.close()

    if (button == {}):

        raise HTTPException(status_code=404)

    return button

def DBCreateButtonInitial(board: int,
                          row_index: int,
                          column_index: int):
    
    connection, cursor = ConnectToDatabase()

    sql = f"INSERT INTO buttons (`board`, `row_index`, `column_index`) \
            VALUES ({board}, {row_index}, {column_index})"
    button_id = None

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)
    
    else:

        button_id = cursor.lastrowid

    finally:

        connection.close()
    
    if (button_id != None):
        
        return DBGetButton(button_id=button_id)

    else:

        return

def DBCreateButton(board: int,
                   row_index: int,
                   column_index: int,
                   label: str,
                   label_color: str,
                   name_color: str,
                   background_color: str,
                   category: int,
                   image: int,
                   is_image_enable: int,
                   voice: int,
                   hyperlink: str,
                   is_hyperlink_inside: int,
                   status: int):

    connection, cursor = ConnectToDatabase()
    if (hyperlink ==""):
        
        sql = f"INSERT INTO buttons ( `board`,`row_index`,`column_index`,`label`,`label_color`,`name_color`,`background_color`,`category`,`image`,`is_image_enable`,`voice`,`hyperlink`,`is_hyperlink_inside`,`status`) \
                VALUES ( '{board}', '{row_index}','{column_index}', '{connection.escape_string(label)}', '{connection.escape_string(label_color)}', '{connection.escape_string(name_color)}', '{connection.escape_string(background_color)}','{category}',{image},'{is_image_enable}',{voice}, NULL, '{is_hyperlink_inside}', '{status}')"
    else:
        
        sql = f"INSERT INTO buttons ( `board`,`row_index`,`column_index`,`label`,`label_color`,`name_color`,`background_color`,`category`,`image`,`is_image_enable`,`voice`,`hyperlink`,`is_hyperlink_inside`,`status`) \
                VALUES ( '{board}', '{row_index}','{column_index}', '{connection.escape_string(label)}', '{connection.escape_string(label_color)}', '{connection.escape_string(name_color)}', '{connection.escape_string(background_color)}','{category}',{image},'{is_image_enable}',{voice}, '{connection.escape_string(hyperlink)}', '{is_hyperlink_inside}', '{status}')"
    button_id = None
    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    else:

        button_id = cursor.lastrowid

    finally:

        connection.close()

    if (button_id == None):

        raise HTTPException(status_code=404)

    return DBGetButton(button_id=button_id)

def DBEditButton(button_id: int,
                 label: str,
                 label_color: str,
                 name_color: str,
                 background_color: str,
                 category: int,
                 image: int,
                 is_image_enable: int,
                 voice: int,
                 hyperlink: str,
                 is_hyperlink_inside: int,
                 status: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM buttons \
            WHERE `id`={button_id}"
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

        raise HTTPException(status_code=404, detail="button_id doesn't exist")
    
    connection, cursor = ConnectToDatabase()
    if (hyperlink ==""):
       
        sql = f"UPDATE buttons \
                SET `label`='{connection.escape_string(label)}', \
                    `label_color`='{connection.escape_string(label_color)}' ,\
                    `name_color`='{connection.escape_string(name_color)}', \
                    `background_color`='{connection.escape_string(background_color)}', \
                    `category`='{category}', \
                    `image`={image}, \
                    `is_image_enable`='{is_image_enable}', \
                    `voice`={voice}, \
                    `hyperlink`= NULL, \
                    `is_hyperlink_inside`='{is_hyperlink_inside}', \
                    `status`='{status}' \
                WHERE`id`={button_id}"
    else:
        
        sql = f"UPDATE buttons \
                SET `label`='{connection.escape_string(label)}', \
                    `label_color`='{connection.escape_string(label_color)}' ,\
                    `name_color`='{connection.escape_string(name_color)}', \
                    `background_color`='{connection.escape_string(background_color)}', \
                    `category`='{category}', \
                    `image`={image}, \
                    `is_image_enable`='{is_image_enable}', \
                    `voice`={voice}, \
                    `hyperlink`='{connection.escape_string(hyperlink)}', \
                    `is_hyperlink_inside`='{is_hyperlink_inside}', \
                    `status`='{status}' \
                WHERE`id`={button_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:
        print(sql)
        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()
    
    return DBGetButton(button_id=button_id)

def DBClearButton(button_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM buttons \
            WHERE `id`={button_id}"
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

        raise HTTPException(status_code=404, detail="button_id doesn't exist")
    
    label_color="#000000"
    name_color="#000000"
    background_color="#FFFFFF"

    connection, cursor = ConnectToDatabase()
    sql = f"UPDATE buttons \
            SET `label`='', \
                `label_color`='{connection.escape_string(label_color)}' ,\
                `name_color`='{connection.escape_string(name_color)}', \
                `background_color`='{connection.escape_string(background_color)}', \
                `category`= 0, \
                `image`= NULL, \
                `is_image_enable`= 0, \
                `voice`= NULL, \
                `hyperlink`= NULL, \
                `is_hyperlink_inside`= 0, \
                `status`= 0 \
            WHERE`id`={button_id}"

    try:

        cursor.execute(sql)

    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code=500)

    finally:

        connection.close()

    return DBGetButton(button_id=button_id)



if __name__ == "__main__":

    print(DBGetButton(button_id= 1936))
    # print(DBShowAllBoardButtons(board_id = 43))
    # print(DBSearchButtonInBoard(board_id=43, board_label="123"))
    # print(DBCreateButton(board=43,
    # row_index=0,
    # column_index=0,
    #label="new button",
    # label_color="#000000",
    # name_color="#000000",
    # background_color="#FFFFFF",
    # category=0,
    # image="NULL",
    # is_image_enable=1,
    # voice="NULL",
    # hyperlink="",
    # is_hyperlink_inside=0,
    # status=0))
    # print(DBEditButton(button_id =1283,
    # label="null",
    # label_color="#000000",
    # name_color="#000000",
    # background_color="#FFFFFF",
    # category=0,
    # image="NULL",
    # is_image_enable=1,
    # voice="NULL",
    # hyperlink="",
    # is_hyperlink_inside=0,
    # status=0))
    # DBClearButton(button_id=1347)
