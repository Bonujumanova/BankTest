from pydantic import BaseModel as BM
from pydantic import ConfigDict
from pydantic import Field

class BaseModel(BM):
    # конструкция нужна для работы alias в дочернем классе
    model_config = ConfigDict(
        populate_by_name=True)
