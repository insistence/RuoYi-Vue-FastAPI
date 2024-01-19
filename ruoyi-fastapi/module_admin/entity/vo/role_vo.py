from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel
from typing import Union, Optional, List
from datetime import datetime
from module_admin.entity.vo.dept_vo import DeptModel
from module_admin.entity.vo.menu_vo import MenuModel


class RoleModel(BaseModel):
    """
    角色表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    role_id: Optional[int] = None
    role_name: Optional[str] = None
    role_key: Optional[str] = None
    role_sort: Optional[int] = None
    data_scope: Optional[str] = None
    menu_check_strictly: Optional[Union[int, bool]] = None
    dept_check_strictly: Optional[Union[int, bool]] = None
    status: Optional[str] = None
    del_flag: Optional[str] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    remark: Optional[str] = None

    @field_validator('menu_check_strictly', 'dept_check_strictly')
    @classmethod
    def check_filed_mapping(cls, v: Union[int, bool]) -> Union[int, bool]:
        if v == 1:
            v = True
        elif v == 0:
            v = False
        elif v is True:
            v = 1
        elif v is False:
            v = 0
        return v


class RoleMenuModel(BaseModel):
    """
    角色和菜单关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    role_id: Optional[int]
    menu_id: Optional[int]


class RoleDeptModel(BaseModel):
    """
    角色和部门关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    role_id: Optional[int]
    dept_id: Optional[int]


class RoleQueryModel(RoleModel):
    """
    角色管理不分页查询模型
    """
    begin_time: Optional[str] = None
    end_time: Optional[str] = None


class RolePageQueryModel(RoleQueryModel):
    """
    角色管理分页查询模型
    """
    page_num: int
    page_size: int
    
    
class RolePageObjectResponse(BaseModel):
    """
    角色管理列表分页查询返回模型
    """
    rows: List[Union[RoleModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class RoleSelectOptionResponseModel(BaseModel):
    """
    角色管理不分页查询模型
    """
    role: List[Union[RoleModel, None]]
    
    
class CrudRoleResponse(BaseModel):
    """
    操作角色响应模型
    """
    is_success: bool
    message: str
    
    
class AddRoleModel(RoleModel):
    """
    新增角色模型
    """
    menu_id: Optional[str]
    type: Optional[str]


class RoleDataScopeModel(RoleModel):
    """
    角色数据权限模型
    """
    dept_id: Optional[str]


class DeleteRoleModel(BaseModel):
    """
    删除角色模型
    """
    role_ids: str
    update_by: Optional[str]
    update_time: Optional[str]
    
    
class RoleDetailModel(BaseModel):
    """
    获取角色详情信息响应模型
    """
    role: Union[RoleModel, None]
    menu: List[Union[MenuModel, None]]
    dept: List[Union[DeptModel, None]]
