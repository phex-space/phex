import pytest
from unittest import mock
from unittest.mock import AsyncMock, MagicMock

import fastapi
from pytest_mock import MockFixture

from phexcore.loader import bootstrap_phexlets, dispose_phexlets, load_phexlets, run_phexlets
from phexcore.protocol import Configuration

_config = Configuration()


@pytest.mark.asyncio
async def test_load_phexlets(app: fastapi.FastAPI, mocker: MockFixture):
    mock_init: MagicMock = mocker.patch("testservices.loader.initialize")
    mock_boot: MagicMock = mocker.patch("testservices.loader.bootstrap")
    mock_run: MagicMock = mocker.patch("testservices.loader.run")
    mock_init2: MagicMock = mocker.patch("testservices.loader2.initialize")
    mock_boot2: MagicMock = mocker.patch("testservices.loader2.bootstrap")
    mock_run2: MagicMock = mocker.patch("testservices.loader2.run")
    services = await load_phexlets(
        ["testservices.loader", "testservices.loader2"], app, _config
    )
    await bootstrap_phexlets(services)
    await run_phexlets(services)

    assert services is not None
    assert len(services) == 2
    mock_init.assert_called_once_with(app, _config)
    mock_boot.assert_called_once()
    mock_run.assert_called_once()
    mock_init2.assert_called_once_with(app, _config)
    mock_boot2.assert_called_once()
    mock_run2.assert_called_once()


@pytest.mark.asyncio
async def test_load_phexlets_async(app: fastapi.FastAPI, mocker: MockFixture):
    mock_init = AsyncMock()
    mocker.patch("testservices.loader_async.initialize", side_effect=mock_init)
    mock_boot = AsyncMock()
    mocker.patch("testservices.loader_async.bootstrap", side_effect=mock_boot)
    mock_run = AsyncMock()
    mocker.patch("testservices.loader_async.run", side_effect=mock_run)
    services = await load_phexlets(["testservices.loader_async"], app, _config)
    await bootstrap_phexlets(services)
    await run_phexlets(services)

    assert services is not None
    assert len(services) == 1
    mock_init.assert_called_once_with(app, _config)
    mock_boot.assert_called_once()
    mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_dispose_phexlets(app: fastapi.FastAPI, mocker: MockFixture):
    mock_disp: MagicMock = mocker.patch("testservices.loader.dispose")
    services = await load_phexlets(["testservices.loader"], app, _config)

    assert services is not None
    assert len(services) == 1
    await dispose_phexlets(services)
    mock_disp.assert_called_once()


@pytest.mark.asyncio
async def test_load_phexlets_suppress_errors(app: fastapi.FastAPI, mocker: MockFixture):
    with pytest.raises(ValueError):
        services = await load_phexlets(["testservices.loader_fail"], app, _config)

    services = await load_phexlets(
        ["testservices.loader_fail"], app, _config, suppress_errors=True
    )

    assert services is not None
    assert len(services) == 1


@pytest.mark.asyncio
async def test_dispose_phexlets_suppress_errors(
    app: fastapi.FastAPI, mocker: MockFixture
):
    services = await load_phexlets(
        ["testservices.loader_fail"], app, _config, suppress_errors=True
    )

    assert services is not None
    assert len(services) == 1
    with pytest.raises(ValueError):
        await dispose_phexlets(services)

    await dispose_phexlets(services, suppress_errors=True)
