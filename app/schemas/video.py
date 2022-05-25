from datetime import date

from pydantic import BaseModel, Field, validator
from slugify import slugify


class VideoBase(BaseModel):
    title: str
    date: date
    yt_id: str
    yt_thumbnail: str
    duration: int
    slug: str = Field(None)


class CreateVideo(VideoBase):
    @validator('slug', always=True)
    def generate_slug(cls, v: str, values: dict) -> str:
        if not v:
            v = slugify(values['title'])
        return v

    class Config:
        fields = {'id': {'exclude': True}}


class PgVideo(VideoBase):
    id: int
    liked: bool = Field(False)


class MeilisearchVideo(VideoBase):
    id: int

    class Config:
        json_encoders = {date: lambda d: int(d.strftime('%s'))}
