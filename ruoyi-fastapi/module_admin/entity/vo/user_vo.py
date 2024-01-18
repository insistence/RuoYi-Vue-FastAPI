from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Union, Optional, List
from datetime import datetime
from module_admin.entity.vo.dept_vo import DeptModel
from module_admin.annotation.form_annotation import as_form


class TokenData(BaseModel):
    """
    token解析结果
    """
    user_id: Union[int, None] = None


class UserModel(BaseModel):
    """
    用户表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    user_id: Optional[int] = None
    dept_id: Optional[int] = None
    user_name: Optional[str] = None
    nick_name: Optional[str] = None
    user_type: Optional[str] = None
    email: Optional[str] = None
    phonenumber: Optional[str] = None
    sex: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    status: Optional[str] = None
    del_flag: Optional[str] = None
    login_ip: Optional[str] = None
    login_date: Optional[datetime] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    remark: Optional[str] = None


class UserRoleModel(BaseModel):
    """
    用户和角色关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    user_id: Optional[int] = None
    role_id: Optional[int] = None


class UserPostModel(BaseModel):
    """
    用户与岗位关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    user_id: Optional[int] = None
    post_id: Optional[int] = None


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
    menu_check_strictly: Optional[int] = None
    dept_check_strictly: Optional[int] = None
    status: Optional[str] = None
    del_flag: Optional[str] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    remark: Optional[str] = None


class PostModel(BaseModel):
    """
    岗位信息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    post_id: Optional[int] = None
    post_code: Optional[str] = None
    post_name: Optional[str] = None
    post_sort: Optional[int] = None
    status: Optional[str] = None
    create_by: Optional[str] = None
    create_time: Optional[datetime] = None
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None
    remark: Optional[str] = None


class CurrentUserInfo(BaseModel):
    """
    数据库返回当前用户信息
    """
    model_config = ConfigDict(alias_generator=to_camel)

    user_basic_info: List[Union[UserModel, None]]
    user_dept_info: List[Union[DeptModel, None]]
    user_role_info: List[Union[RoleModel, None]]
    user_post_info: List[Union[PostModel, None]]
    user_menu_info: Union[List, None]


class UserInfoModel(UserModel):
    post_ids: Union[str, None]
    role_ids: Union[str, None]
    dept: Union[DeptModel, None]
    role: List[Union[RoleModel, None]]


class CurrentUserModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    permissions: List
    roles: List
    user: Union[UserInfoModel, None]


class UserDetailModel(BaseModel):
    """
    获取用户详情信息响应模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    data: Optional[Union[UserInfoModel, None]] = None
    post_ids: Optional[List] = None
    posts: List[Union[PostModel, None]]
    role_ids: Optional[List] = None
    roles: List[Union[RoleModel, None]]


class UserProfileModel(BaseModel):
    """
    获取个人信息响应模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    data: Union[UserInfoModel, None]
    post_group: Union[str, None]
    role_group: Union[str, None]


class CurrentUserInfoServiceResponse(UserDetailModel):
    """
    获取当前用户信息响应模型
    """
    menu: Union[List, None]


class UserQueryModel(UserModel):
    """
    用户管理不分页查询模型
    """
    begin_time: Optional[str] = None
    end_time: Optional[str] = None


@as_form
class UserPageQueryModel(UserQueryModel):
    """
    用户管理分页查询模型
    """
    page_num: int
    page_size: int


class AddUserModel(UserModel):
    """
    新增用户模型
    """
    role_ids: Optional[List] = []
    post_ids: Optional[List] = []
    type: Optional[str] = None


class EditUserModel(AddUserModel):
    """
    编辑用户模型
    """
    role: Optional[List] = []


class ResetUserModel(UserModel):
    """
    重置用户密码模型
    """
    old_password: Optional[str] = None
    sms_code: Optional[str] = None
    session_id: Optional[str] = None


class DeleteUserModel(BaseModel):
    """
    删除用户模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    user_ids: str
    update_by: Optional[str] = None
    update_time: Optional[datetime] = None


class UserRoleQueryModel(UserRoleModel):
    """
    用户角色关联管理不分页查询模型
    """
    user_name: Optional[str] = None
    phonenumber: Optional[str] = None
    role_name: Optional[str] = None
    role_key: Optional[str] = None


class UserRolePageObject(UserRoleQueryModel):
    """
    用户角色关联管理分页查询模型
    """
    page_num: int
    page_size: int


class UserRolePageObjectResponse(BaseModel):
    """
    用户角色关联管理列表分页查询返回模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    rows: List = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class CrudUserRoleModel(BaseModel):
    """
    新增、删除用户关联角色及角色关联用户模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    user_ids: Optional[str] = None
    role_ids: Optional[str] = None


class ImportUserModel(BaseModel):
    """
    批量导入用户模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    url: str
    is_update: bool


class CrudUserResponse(BaseModel):
    """
    操作用户响应模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    is_success: bool
    message: str


class DeptInfo(BaseModel):
    """
    查询部门树
    """
    model_config = ConfigDict(alias_generator=to_camel)

    dept_id: int
    dept_name: str
    ancestors: str


class RoleInfo(BaseModel):
    """
    用户角色信息
    """
    model_config = ConfigDict(alias_generator=to_camel)

    role_info: Union[List, None]


class MenuList(BaseModel):
    """
    用户菜单信息
    """
    model_config = ConfigDict(alias_generator=to_camel)

    menu_info: Union[List, None]
