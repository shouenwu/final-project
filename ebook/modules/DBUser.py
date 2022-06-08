import mariadb
from fastapi import HTTPException


from modules.ConnectToDatabase import ConnectToDatabase


def DBSearchUser(account: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, nickname, account, role, email, department, created_time \
            FROM users \
            WHERE account LIKE '%{connection.escape_string(account)}%'"
    users = []

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:
        
        for (id, name, nickname, account, role, email, department, created_time) in cursor:

            user = {"id": id,
                    "name": name,
                    "nickname": nickname,
                    "account": account,
                    "role": role,
                    "email": email,
                    "department": department,
                    "created_time": created_time}
            users.append(user)

    finally:

        connection.close()

    return users

def DBGetUser(user_id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id, name, nickname, account, password, role, email, department, created_time \
            FROM users \
            WHERE `id`={user_id}"
    user = {}    

    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (id, name, nickname, account, password, role, email, department, created_time) in cursor:

            user = {"id": id,
                    "name": name,
                    "nickname": nickname,
                    "account": account,
                    "password": password,
                    "role": role,
                    "email": email,
                    "department": department,
                    "created_time": created_time}
    
    finally:

        connection.close()
    
    if (user == {}):

        raise HTTPException(status_code = 404)
    
    return user

def DBCreateUser(name: str,
                 nickname: str,
                 account: str,
                 password: str,
                 role: str,
                 email: str,
                 department: str):

    connection, cursor = ConnectToDatabase()
    sql = f"SELECT id \
            FROM users \
            WHERE `account`='{account}'"
    whether_account_exist = False
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        for (id) in cursor:

            whether_account_exist = True
    
    finally:

        connection.close()
    
    if (whether_account_exist == True):

        raise HTTPException(status_code = 400, detail = "account already exists")

    connection, cursor = ConnectToDatabase()
    sql = f"INSERT INTO users (`name`, `nickname`, `account`, `password`, `role`, `email`, `department`, `created_time`) \
            VALUES ('{connection.escape_string(name)}', '{connection.escape_string(nickname)}', '{connection.escape_string(account)}', '{connection.escape_string(password)}','{connection.escape_string(role)}', '{connection.escape_string(email)}', '{connection.escape_string(department)}', now())"
    print(sql)
    user_id = None
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    else:

        user_id = cursor.lastrowid
    
    finally:

        connection.close()
    
    if (user_id == None):

        raise HTTPException(status_code = 404)

    return DBGetUser(user_id = user_id)

def DBEditUser(id: int,
               name: str,
               nickname: str,
               account: str,
               password: str,
               role: str,
               email: str,
               department: str):

    connection, cursor = ConnectToDatabase()
    sql = f"UPDATE users \
            SET `name`='{connection.escape_string(name)}', \
                `nickname`='{connection.escape_string(nickname)}', \
                `account`='{connection.escape_string(account)}', \
                `password`='{connection.escape_string(password)}', \
                `role`='{connection.escape_string(role)}', \
                `email`='{connection.escape_string(email)}', \
                `department`='{connection.escape_string(department)}' \
            WHERE `id`={id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return DBGetUser(user_id = id)

def DBDeleteUser(id: int):

    connection, cursor = ConnectToDatabase()
    sql = f"DELETE FROM users \
            WHERE `id`={id}"
    
    try:

        cursor.execute(sql)
    
    except mariadb.Error as e:

        print(e)
        raise HTTPException(status_code = 500)
    
    finally:

        connection.close()

    return 

if __name__ == "__main__":

    print(DBSearchUser(account = "apex"))
    # test case
    # get single user data 
    try:

        print(DBGetUser(user_id = 2))

    except HTTPException as e:

        print(e.status_code)

    # test case
    # create new user data 
    try:

        user = DBCreateUser(name =  "this is temp testing user",
                           nickname = "temp",
                           account = "temp",
                           password = "temp",
                           role = "admin",
                           email = "",
                           department = "")
    
    except HTTPException as e:

        print(e.detail)

    else:

        print(user)
        id = user['id']

    # test case
    # edit user data
    # try:

    #     print(DBEditUser(id = id,
    #                      name = "edit test",
    #                      nickname = "temp",
    #                      account = "temp",
    #                      password = "temp",
    #                      role = "admin",
    #                      email = "",
    #                      department = ""))
    
    # except HTTPException as e:

    #     print(e.status_code)
    
    # test case
    # delete user data
    # try:

    #     DBDeleteUser(id = id)
    
    # except HTTPException as e:

    #     print(e.status_code)