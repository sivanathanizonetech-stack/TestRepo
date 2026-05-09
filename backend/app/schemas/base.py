from pydantic import BaseModel


class SchemaModel(BaseModel):
    def model_dump(self, *args, **kwargs):
        return self.dict(*args, **kwargs)

