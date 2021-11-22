import fastapi
from fastapi import Depends

from phex.authentication import approve
from phex.oidc import Access
from phex.pkg import controller
from .schema import Package

router = fastapi.APIRouter(prefix="/pkg")


@router.get("", response_model=list[Package])
async def list_packages(_=Depends(approve(Access("read", "package")))) -> list[Package]:
    return await controller.list_packages()


@router.post("", response_model=Package)
async def create_package(
    package: Package,
    _=Depends(approve(Access("read", "package"), Access("write", "package"))),
) -> Package:
    return await controller.create_package(package)


@router.get(
    "/{package_id}",
    response_model=Package,
    response_model_exclude_unset=False,
    response_model_exclude_none=True,
)
async def read_package(
    package_id: str, _=Depends(approve(Access("read", "package")))
) -> Package:
    return await controller.read_package(package_id)


@router.put("/{package_id}", response_model=Package)
async def update_package(package_id: str, package: Package) -> Package:
    return await controller.update_package(package_id, package)


@router.delete("/{package_id}", response_model=Package)
async def delete_package(package_id: str) -> Package:
    return await controller.delete_package(package_id)
