from typing import Optional
import mariadb
from fastapi.exceptions import HTTPException

import modules.DBEbook as DBEbook


async def AuthEditEbookPermission(id: int, user: dict):

    ebook = DBEbook.DBUseIdGetEbook(ebook_id = id)
    
    if (ebook["privacy"] == "public"):

        raise HTTPException(status_code= 403)
    
    elif (ebook['privacy'] == "private"
          and ebook['creator'] != user['id']):

        raise HTTPException(status_code= 403)