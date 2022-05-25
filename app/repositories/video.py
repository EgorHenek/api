from abc import ABC, abstractmethod
from typing import Coroutine, Any

from fastapi.encoders import jsonable_encoder
from meilisearch_python_async.task import wait_for_task
from pydantic import parse_obj_as

from app.meilisearch import MeilisearchRepository
from app.schemas.video import MeilisearchVideo, VideoBase


class VideoRepository(ABC):
    @abstractmethod
    def create(self, video: VideoBase) -> Coroutine[Any, Any, VideoBase]:
        pass

    @abstractmethod
    def delete(self, id_: int) -> Coroutine[Any, Any, None]:
        pass

    @abstractmethod
    def get_all(
            self,
            *,
            limit: int = 20,
            offset: int = 0
    ) -> list[VideoBase | None]:
        pass

    @abstractmethod
    def get_by_id(self, id_: int) -> Coroutine[Any, Any, VideoBase]:
        pass

    @abstractmethod
    def update(self, video: VideoBase) -> Coroutine[Any, Any, VideoBase]:
        pass

    @abstractmethod
    def delete_all(self) -> Coroutine[Any, Any, None]:
        pass


class MeilisearchVideoRepository(VideoRepository, MeilisearchRepository):
    def __init__(self) -> None:
        index_name = self._normalize_index_name("videos")
        self.index = self.client.index(index_name)

    async def create(  # type: ignore[override]
            self,
            video: MeilisearchVideo
    ) -> MeilisearchVideo:
        documents = [jsonable_encoder(video)]
        task = await self.index.add_documents(documents)
        await wait_for_task(self.client.http_client, task.uid)
        return video

    async def delete(self, id_: int) -> None:
        task = await self.index.delete_document(str(id_))
        await wait_for_task(self.client.http_client, task.uid)

    async def get_all(  # type: ignore[override]
            self,
            *,
            limit: int = 20,
            offset: int = 0
    ) -> list[MeilisearchVideo | None]:
        documents = await self.index.get_documents(limit=limit, offset=offset)
        if documents:
            return parse_obj_as(
                list[MeilisearchVideo],  # type: ignore
                documents
            )
        return []

    async def get_by_id(self, id_: int) -> MeilisearchVideo:
        document = await self.index.get_document(str(id_))
        return MeilisearchVideo.parse_obj(document)

    async def update(  # type: ignore[override]
            self,
            video: MeilisearchVideo,
    ) -> MeilisearchVideo:
        await self.create(video)
        return video

    async def delete_all(self) -> None:
        task = await self.clear_index(self.index)
        await wait_for_task(self.client.http_client, task.uid)


meilisearch_video_repository = MeilisearchVideoRepository()
