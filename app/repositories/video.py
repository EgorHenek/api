from abc import ABC, abstractmethod
from typing import Any, Coroutine

from databases import Database
from fastapi.encoders import jsonable_encoder
from meilisearch_python_async import Client as MeilisearchClient
from meilisearch_python_async.errors import MeiliSearchApiError
from meilisearch_python_async.task import wait_for_task
from pydantic import parse_obj_as
from sqlalchemy import desc, func, select
from sqlalchemy.sql.expression import false

from app.db import videos
from app.meilisearch import normalize_ms_index_name
from app.schemas.video import (
    CreateVideo,
    DbVideo,
    MeilisearchVideo,
    PgVideo,
    VideoBase,
)


class VideoRepository(ABC):
    @abstractmethod
    def create(
        self,
        video: CreateVideo,
    ) -> Coroutine[Any, Any, DbVideo]:
        pass

    @abstractmethod
    def delete(
        self,
        id_: int,
    ) -> Coroutine[Any, Any, None]:
        pass

    @abstractmethod
    def get_all(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> Coroutine[Any, Any, list[DbVideo | None]]:
        pass

    @abstractmethod
    def get_by_id(
        self,
        id_: int,
    ) -> Coroutine[Any, Any, DbVideo | None]:
        pass

    @abstractmethod
    def get_by_slug(
        self,
        slug: str,
    ) -> Coroutine[Any, Any, DbVideo | None]:
        pass

    @abstractmethod
    def get_by_yt_id(
        self,
        yt_id: str,
    ) -> Coroutine[Any, Any, DbVideo | None]:
        pass

    @abstractmethod
    def update(
        self,
        video: DbVideo,
    ) -> Coroutine[Any, Any, DbVideo]:
        pass

    @abstractmethod
    def count(self) -> Coroutine[Any, Any, int]:
        pass


class MeilisearchVideoRepository(VideoRepository):
    def __init__(self, client: MeilisearchClient) -> None:
        self.client = client
        index_name = normalize_ms_index_name("videos")
        self.index = self.client.index(index_name)

    async def create(  # type: ignore[override]
        self,
        video: MeilisearchVideo,
    ) -> MeilisearchVideo:
        documents = [jsonable_encoder(video)]
        task = await self.index.add_documents(documents)
        await wait_for_task(self.client.http_client, task.uid)
        return video

    async def delete(
        self,
        id_: int,
    ) -> None:
        task = await self.index.delete_document(str(id_))
        await wait_for_task(self.client.http_client, task.uid)

    async def get_all(  # type: ignore[override]
        self,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> list[MeilisearchVideo | None]:
        documents = await self.index.get_documents(limit=limit, offset=offset)
        if documents:
            return parse_obj_as(
                list[MeilisearchVideo], documents  # type: ignore
            )
        return []

    async def get_by_id(
        self,
        id_: int,
    ) -> MeilisearchVideo | None:
        try:
            document = await self.index.get_document(str(id_))
            return MeilisearchVideo.parse_obj(document)
        except MeiliSearchApiError as e:
            if e.code == "document_not_found":
                return None
            raise e

    async def get_by_slug(
        self,
        slug: str,
    ) -> MeilisearchVideo | None:
        result = await self.index.search(filter=f"slug = {slug}")
        if result.nb_hits == 0:
            return None
        return MeilisearchVideo.parse_obj(result.hits[0])

    async def get_by_yt_id(
        self,
        yt_id: str,
    ) -> MeilisearchVideo | None:
        result = await self.index.search(filter=f"yt_id = {yt_id}")
        if result.nb_hits == 0:
            return None
        return MeilisearchVideo.parse_obj(result.hits[0])

    async def update(  # type: ignore[override]
        self,
        video: MeilisearchVideo,
    ) -> MeilisearchVideo:
        await self.create(video)
        return video

    async def count(self) -> int:
        stats = await self.index.get_stats()
        return stats.number_of_documents


class PostgresVideoRepository(VideoRepository):
    def __init__(self, session: Database) -> None:
        self.__session = session

    async def create(
        self,
        video: CreateVideo,
    ) -> PgVideo:
        query = videos.insert().returning(videos)
        db_video = await self.__session.fetch_one(
            query=query,
            values=video.dict(),
        )
        return PgVideo.parse_obj(db_video)

    async def delete(
        self,
        id_: int,
    ) -> None:
        query = videos.update().where(videos.c.id == id_)
        await self.__session.execute(query=query, values={"deleted": True})
        return None

    async def get_all(  # type: ignore[override]
        self,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> list[PgVideo | None]:
        query = (
            videos.select()
            .where(videos.c.deleted == false())
            .order_by(desc("date"))
            .order_by(desc("id"))
            .limit(limit)
            .offset(offset)
        )
        db_videos = await self.__session.fetch_all(query=query)
        return parse_obj_as(
            list[PgVideo],  # type: ignore
            db_videos,
        )

    async def get_by_id(
        self,
        id_: int,
    ) -> PgVideo | None:
        query = (
            videos.select()
            .where(videos.c.id == id_)
            .where(videos.c.deleted == false())
        )
        db_video = await self.__session.fetch_one(query=query)
        if db_video:
            return PgVideo.parse_obj(db_video)
        return None

    async def get_by_slug(
        self,
        slug: str,
    ) -> PgVideo | None:
        query = (
            videos.select()
            .where(videos.c.slug == slug)
            .where(videos.c.deleted == false())
        )
        db_video = await self.__session.fetch_one(query=query)
        if db_video:
            return PgVideo.parse_obj(db_video)
        return None

    async def get_by_yt_id(
        self,
        yt_id: str,
    ) -> PgVideo | None:
        query = (
            videos.select()
            .where(videos.c.yt_id == yt_id)
            .where(videos.c.deleted == false())
        )
        db_video = await self.__session.fetch_one(query=query)
        if db_video:
            return PgVideo.parse_obj(db_video)
        return None

    async def update(  # type: ignore[override]
        self,
        video: PgVideo,
    ) -> VideoBase:
        query = videos.update().where(videos.c.id == video.id)
        await self.__session.execute(
            query=query,
            values=video.dict(exclude_defaults=True),
        )
        return video

    async def count(self) -> int:
        query = (
            select([func.count()])
            .select_from(videos)
            .where(videos.c.deleted == false())
        )
        return int(await self.__session.fetch_val(query=query))
