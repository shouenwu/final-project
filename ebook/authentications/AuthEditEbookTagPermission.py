from fastapi import HTTPException



import modules.DBEbookTag as DBEbookTag



async def AuthEditEbookTagPermission(tag_id: int,
                                     user: dict):

    ebook_tag = DBEbookTag.DBGetEbookTag(ebook_tag_id = tag_id)

    if (ebook_tag['creator'] != user['id']):

        raise HTTPException(status_code=403)