import logging
import fastapi
import pytest
import sqlalchemy

from phexcore import loader, services
from phexcore.database import DatabaseService
from phexcore.protocol import Configuration

_logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_database_service(app: fastapi.FastAPI, db_url: str):
    config = Configuration(database_url=db_url)
    phexlets = await loader.load_phexlets(
        ["phexcore.database", "testservices.entities"], app, config
    )
    await loader.bootstrap_phexlets(phexlets)
    await loader.run_phexlets(phexlets)

    db: DatabaseService = services.get("database")
    assert db is not None
    Post = services.get("Post")
    assert Post is not None

    await loader.dispose_phexlets(phexlets)


@pytest.mark.asyncio
async def test_database_service_session(app: fastapi.FastAPI, db_url: str):
    config = Configuration(database_url=db_url)
    phexlets = await loader.load_phexlets(
        ["phexcore.database", "testservices.entities"], app, config
    )
    await loader.bootstrap_phexlets(phexlets)
    await loader.run_phexlets(phexlets)

    Post = services.get("Post")

    db: DatabaseService = services.get("database")
    with db.new_session() as session:

        post = Post(id=42, title="Test Post", content="Test Post Content")
        session.add(post)
        session.commit()
        session.refresh(post)

        assert post.id == 42
        assert post.title == "Test Post"
        assert post.content == "Test Post Content"

        retrieved_post = session.query(Post).get(42)
        assert retrieved_post.id == 42
        assert retrieved_post.title == "Test Post"
        assert retrieved_post.content == "Test Post Content"

        raw_dict = retrieved_post._asdict()
        assert raw_dict is not None
        assert raw_dict.get("id") == 42
        assert raw_dict.get("title") == "Test Post"
        assert raw_dict.get("content") == "Test Post Content"

    await loader.dispose_phexlets(phexlets)
