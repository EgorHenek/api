from typing import Mapping

import pytest

from app.repositories.video import (
    MeilisearchVideoRepository,
    PostgresVideoRepository,
)
from app.schemas.video import CreateVideo, MeilisearchVideo, PgVideo


class TestMeilisearchVideoRepository:
    @pytest.mark.asyncio
    async def test_create(
        self,
        pg_video: PgVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        video = MeilisearchVideo(**pg_video.dict())
        await ms_video_repository.create(video)

        assert await ms_video_repository.get_by_id(video.id)

    @pytest.mark.asyncio
    async def test_delete(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        await ms_video_repository.delete(ms_video.id)
        assert await ms_video_repository.get_by_id(ms_video.id) is None

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        result = await ms_video_repository.get_all()
        assert type(result) == list
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        assert await ms_video_repository.get_by_id(ms_video.id)

    @pytest.mark.asyncio
    async def test_get_nonexistent_id(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        assert await ms_video_repository.get_by_id(ms_video.id + 1) is None

    @pytest.mark.asyncio
    async def test_update(
        self,
        ms_video: MeilisearchVideo,
        videos: list[Mapping],
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        video = ms_video.copy()
        video.title = "New title"
        await ms_video_repository.update(video)
        updated_video = await ms_video_repository.get_by_id(video.id)
        assert updated_video != ms_video

    @pytest.mark.asyncio
    async def test_get_by_slug(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        assert await ms_video_repository.get_by_slug(ms_video.slug)

    @pytest.mark.asyncio
    async def test_get_nonexistent_slug(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        assert (
            await ms_video_repository.get_by_slug(ms_video.slug + "1") is None
        )

    @pytest.mark.asyncio
    async def test_get_by_yt_id(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        assert await ms_video_repository.get_by_yt_id(ms_video.yt_id)

    @pytest.mark.asyncio
    async def test_get_by_yt_id_nonexistent(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        assert (
            await ms_video_repository.get_by_yt_id(ms_video.yt_id + "1")
            is None
        )

    @pytest.mark.asyncio
    async def test_count(
        self,
        ms_video: MeilisearchVideo,
        ms_video_repository: MeilisearchVideoRepository,
    ) -> None:
        assert await ms_video_repository.count() > 1


class TestPostgresVideoRepository:
    @pytest.mark.asyncio
    async def test_create(
        self,
        video_data: dict,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        video = CreateVideo(**video_data)
        pg_video = await pg_video_repository.create(video)

        assert pg_video.id is not None
        assert pg_video.slug == video.slug

        assert await pg_video_repository.get_by_id(pg_video.id)

    @pytest.mark.asyncio
    async def test_delete(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        await pg_video_repository.delete(pg_video.id)
        assert await pg_video_repository.get_by_id(pg_video.id) is None

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        result = await pg_video_repository.get_all()
        assert type(result) == list
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        assert await pg_video_repository.get_by_id(pg_video.id)

    @pytest.mark.asyncio
    async def test_get_by_nonexistent_id(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        assert await pg_video_repository.get_by_id(pg_video.id + 1) is None

    @pytest.mark.asyncio
    async def test_get_by_slug(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        assert await pg_video_repository.get_by_slug(pg_video.slug)

    @pytest.mark.asyncio
    async def test_get_nonexistent_slug(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        assert (
            await pg_video_repository.get_by_slug(pg_video.slug + "1") is None
        )

    @pytest.mark.asyncio
    async def test_get_by_yt_id(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        assert await pg_video_repository.get_by_yt_id(pg_video.yt_id)

    @pytest.mark.asyncio
    async def test_get_nonexistent_yt_id(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        assert (
            await pg_video_repository.get_by_yt_id(pg_video.yt_id + "1")
            is None
        )

    @pytest.mark.asyncio
    async def test_update(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        video = pg_video.copy()
        video.title = "New title"

        await pg_video_repository.update(video)
        updated_video = await pg_video_repository.get_by_id(video.id)
        assert updated_video != pg_video

    @pytest.mark.asyncio
    async def test_count(
        self,
        pg_video: PgVideo,
        pg_video_repository: PostgresVideoRepository,
    ) -> None:
        assert await pg_video_repository.count() == 1
