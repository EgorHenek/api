from typing import Mapping

import pytest
from meilisearch_python_async.errors import MeiliSearchApiError

from app.repositories.video import meilisearch_video_repository
from app.schemas.video import MeilisearchVideo


class TestMeilisearchVideoRepository:
    @pytest.mark.asyncio
    async def test_create(self, videos: list[Mapping]) -> None:
        video = MeilisearchVideo(**videos[0])
        await meilisearch_video_repository.create(video)

        assert await meilisearch_video_repository.get_by_id(video.id)

    @pytest.mark.asyncio
    async def test_delete(
            self,
            ms_video: MeilisearchVideo
    ) -> None:
        await meilisearch_video_repository.delete(ms_video.id)
        with pytest.raises(MeiliSearchApiError):
            await meilisearch_video_repository.get_by_id(ms_video.id)

    @pytest.mark.asyncio
    async def test_get_all(self, ms_video: MeilisearchVideo) -> None:
        result = await meilisearch_video_repository.get_all()
        assert type(result) == list
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_by_id(self, ms_video: MeilisearchVideo) -> None:
        assert await meilisearch_video_repository.get_by_id(ms_video.id)

    @pytest.mark.asyncio
    async def test_update(
            self,
            ms_video: MeilisearchVideo,
            videos: list[Mapping]
    ) -> None:
        video = ms_video.copy()
        video.title = "New title"
        await meilisearch_video_repository.update(video)
        updated_video = await meilisearch_video_repository.get_by_id(video.id)
        assert updated_video != ms_video

    @pytest.mark.asyncio
    async def test_delete_all(
            self,
            ms_video: MeilisearchVideo,
    ) -> None:
        await meilisearch_video_repository.delete_all()
        with pytest.raises(MeiliSearchApiError):
            await meilisearch_video_repository.get_by_id(ms_video.id)
        assert not await meilisearch_video_repository.get_all()
