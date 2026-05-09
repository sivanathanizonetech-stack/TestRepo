from pydantic import BaseModel


class SchemaModel(BaseModel):
    class Config:
        orm_mode = True

    def model_dump(self, *args, **kwargs):
        return self.dict(*args, **kwargs)
