from fastapi import HTTPException

import mariadb



def ConnectToDatabase():

    try:

        connection = mariadb.connect(
            user="superui",
            password="password_here",
            host="localhost",
            port=3306,
            database="aac",
            autocommit=True
        )    
    
    except mariadb.OperationalError as e:

        print(f"{e}")
        raise HTTPException(status_code=500)

    except mariadb.Error as e:
        
        print(f"{e}")
        raise HTTPException(status_code = 500)

    else:

        return connection, connection.cursor()


if __name__ == "__main__":

    connection, cursor = ConnectToDatabase()