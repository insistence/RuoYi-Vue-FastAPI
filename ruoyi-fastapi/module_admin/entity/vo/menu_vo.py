from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from datetime import datetime
from typing import Union, Optional, List


class MenuModel(BaseModel):
    """
    菜单表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    menu_id: Optional[int] = None
    menu_name: Optional[str] = None
    parent_id: Optional[int] = None
    order_num: Optional[int] = None
    path: Optional[str] = None
    component: Optional[str] = None
    query: Optional[str] = None
    is_frame: Optional[int] = None
    is_cache: Optional[int] = None
    menu_type: Optional[str] = None
    visible: Optional[str] = None
    status: Optional[str] = None
    perms: Optional[str] = None
    icon: Optional[str] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    remark: Optional[str] = None
        
        
class MenuTreeModel(MenuModel):
    """
    菜单树查询模型
    """
    type: Optional[str] = None


class RoleMenuQueryModel(BaseModel):
    """
    角色菜单查询模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    menus: List = []
    checked_keys: List[int] = []


class MenuPageObject(MenuModel):
    """
    菜单管理分页查询模型
    """
    page_num: int
    page_size: int


class MenuPageObjectResponse(BaseModel):
    """
    菜单管理列表分页查询返回模型
    """
    rows: List[Union[MenuModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class MenuResponse(BaseModel):
    """
    菜单管理列表不分页查询返回模型
    """
    rows: List[Union[MenuModel, None]] = []


class MenuTree(BaseModel):
    """
    菜单树响应模型
    """
    menu_tree: Union[List, None]


class CrudMenuResponse(BaseModel):
    """
    操作菜单响应模型
    """
    is_success: bool
    message: str


class DeleteMenuModel(BaseModel):
    """
    删除菜单模型
    """
    menu_ids: str
