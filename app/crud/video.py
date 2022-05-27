from typing import Mapping

from sqlalchemy import case, exists, select
from sqlalchemy.sql.elements import Label

from app.db import database, liked_videos, videos


def is_liked(user_id: int) -> Label:
    return case(
        [
            (
                exists(
                    select([liked_videos])
                    .where(liked_videos.c.video_id == videos.c.id)
                    .where(liked_videos.c.user_id == user_id)
                ),
                "t",
            )
        ],
        else_="f",
    ).label("liked")


async def get_related_videos(
    title: str,
    limit: int = 25,
    user_id: int = None,
    deleted: bool = False,
) -> list[Mapping]:
    selected_tables = [videos]
    if user_id:
        selected_tables.append(is_liked(user_id))

    query = select(selected_tables).where(videos.c.deleted == deleted)
    query = query.order_by(videos.c.title.op("<->")(title))
    query = query.limit(limit).offset(1)
    return await database.fetch_all(query=query)
