from pydantic import BaseModel


class FileModel(BaseModel):
    file_name:str
    destination_file_name:str

class QueueMessageModel(BaseModel):
    message_content:str

class TableEntityModel(BaseModel):
    partition_key:str
    row_key:str
    name:str
    age:int

