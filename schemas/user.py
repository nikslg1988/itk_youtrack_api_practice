from pydantic import BaseModel


class UserMe(BaseModel):
    id: str
    login: str
    name: str
