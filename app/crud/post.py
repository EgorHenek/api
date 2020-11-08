import typing
from datetime import datetime

from sqlalchemy import desc, select, func

from app.db import posts, database
from app.schemas.post import BasePost


async def create_post(post: BasePost, user_id: int) -> typing.Mapping:
    query = posts.insert().returning(posts)
    post = post.dict()
    post['published_at'] = post['published_at'].replace(tzinfo=None)
    post['user_id'] = user_id
    return await database.fetch_one(query=query, values=post)


async def get_post_by_slug(slug: str) -> typing.Mapping:
    query = posts.select().where(posts.c.slug == slug)
    query = query.where(posts.c.published_at <= datetime.now())
    return await database.fetch_one(query=query)


async def get_posts(
        skip: int = 0,
        limit: int = 12,
) -> typing.List[typing.Mapping]:
    query = posts.select()
    query = query.where(posts.c.published_at <= datetime.now())
    query = query.order_by(desc(posts.c.published_at))
    query = query.offset(skip).limit(limit)
    return await database.fetch_all(query=query)


async def get_posts_count() -> int:
    query = select([func.count()]).select_from(posts)
    query = query.where(posts.c.published_at <= datetime.now())
    return await database.fetch_val(query)


async def delete_post(slug: str) -> bool:
    query = posts.delete().where(posts.c.slug == slug).returning(posts)
    return bool(await database.execute(query=query))
