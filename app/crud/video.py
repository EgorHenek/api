import typing

from sqlalchemy import desc, select, func, case, exists, and_
from sqlalchemy.sql.elements import Label

from app.db import videos, database, liked_videos
from app.helpers import algolia_client


def is_liked(user_id: int) -> Label:
    return case([
        (exists(select([liked_videos]).where(liked_videos.c.video_id == videos.c.id).where(
            liked_videos.c.user_id == user_id)), 't')
    ], else_='f').label('liked')


async def add_video(title: str, slug: str, yt_id: str, yt_thumbnail: str, date=None, channel_id: int = None,
                    duration: int = 0):
    query = videos.insert().returning()
    values = {'title': title, 'slug': slug, 'yt_id': yt_id, 'yt_thumbnail': yt_thumbnail, 'date': date,
              'channel_id': channel_id, 'duration': duration}
    db_video = await database.fetch_one(query=query, values=values)
    if db_video:
        index = algolia_client()
        index.save_object(
            {'objectID': db_video['id'], 'title': title, 'date': date, 'slug': slug, 'thumbnail': yt_thumbnail})
    return db_video


async def get_videos_count(deleted: bool = False, parent=None) -> int:
    query = select([func.count()]).select_from(videos).where(videos.c.deleted == deleted)
    return await database.fetch_val(query=query)


async def get_videos(skip: int = 0, limit: int = 25, channel_id: int = None, deleted: bool = False,
                     user_id: int = None) -> typing.List[typing.Mapping]:
    selected_tables = [videos]
    if user_id:
        selected_tables.append(is_liked(user_id))

    query = select(selected_tables).where(videos.c.deleted == deleted)
    if channel_id:
        query = query.where(videos.c.channel_id == channel_id)
    query = query.order_by(desc('date'))
    query = query.offset(skip).limit(limit)
    return await database.fetch_all(query=query)


async def get_related_videos(title: str, limit: int = 25, user_id: int = None,
                             deleted: bool = False) -> typing.List[typing.Mapping]:
    selected_tables = [videos]
    if user_id:
        selected_tables.append(is_liked(user_id))

    query = select(selected_tables).where(videos.c.deleted == deleted).order_by(videos.c.title.op('<->')(title)).limit(
        limit)
    return await database.fetch_all(query=query)


async def get_liked_videos(user_id: int) -> typing.List[typing.Mapping]:
    query = liked_videos.join(videos, and_(videos.c.id == liked_videos.c.video_id, videos.c.deleted == False))
    query = select([videos]).select_from(query)
    query = query.where(liked_videos.c.user_id == user_id)
    return await database.fetch_all(query=query)


async def like_video(user_id: int, video_id: int) -> bool:
    query = liked_videos.insert()
    values = {'user_id': user_id, 'video_id': video_id}
    return bool(await database.execute(query=query, values=values))


async def dislike_video(user_id: int, video_id: int) -> bool:
    query = liked_videos.delete().where(liked_videos.c.user_id == user_id).where(
        liked_videos.c.video_id == video_id).returning(liked_videos)
    return bool(await database.fetch_one(query))


async def get_video_by_slug(slug: str, deleted: bool = False, user_id: int = None) -> typing.Mapping:
    selected_tables = [videos]
    if user_id:
        selected_tables.append(is_liked(user_id))

    query = select(selected_tables).where(videos.c.slug == slug).where(videos.c.deleted == deleted)
    return await database.fetch_one(query=query)


async def delete_video(video_id: int) -> bool:
    query = videos.update().where(videos.c.id == video_id).returning(videos)
    return bool(await database.fetch_one(query=query, values={'deleted': True}))
