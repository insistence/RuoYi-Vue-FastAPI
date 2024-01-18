from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Union, Optional, List
from datetime import datetime


class DeptModel(BaseModel):
    """
    部门表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    dept_id: Optional[int] = None
    parent_id: Optional[int] = None
    ancestors: Optional[str] = None
    dept_name: Optional[str] = None
    order_num: Optional[int] = None
    leader: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    del_flag: Optional[str] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None


class DeptPageObject(DeptModel):
    """
    部门管理分页查询模型
    """
    page_num: int
    page_size: int


class DeptResponse(BaseModel):
    """
    用户管理列表不分页查询返回模型
    """
    rows: List[Union[DeptModel, None]] = []


class DeptTree(BaseModel):
    """
    部门树响应模型
    """
    dept_tree: Union[List, None]


class CrudDeptResponse(BaseModel):
    """
    操作部门响应模型
    """
    is_success: bool
    message: str


class DeleteDeptModel(BaseModel):
    """
    删除部门模型
    """
    dept_ids: str
    update_by: Optional[str]
    update_time: Optional[str]
