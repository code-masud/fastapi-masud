from pydantic import BaseModel, ConfigDict

class LikeRequest(BaseModel):
    post_id: int
    like: bool

    model_config = ConfigDict(from_attributes=True)