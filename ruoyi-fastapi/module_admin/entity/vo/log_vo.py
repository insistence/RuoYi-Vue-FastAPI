from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Union, Optional, List
from datetime import datetime


class OperLogModel(BaseModel):
    """
    操作日志表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    oper_id: Optional[int] = None
    title: Optional[str] = None
    business_type: Optional[int] = None
    method: Optional[str] = None
    request_method: Optional[str] = None
    operator_type: Optional[int] = None
    oper_name: Optional[str] = None
    dept_name: Optional[str] = None
    oper_url: Optional[str] = None
    oper_ip: Optional[str] = None
    oper_location: Optional[str] = None
    oper_param: Optional[str] = None
    json_result: Optional[str] = None
    status: Optional[int] = None
    error_msg: Optional[str] = None
    oper_time: Optional[datetime] = None
    cost_time: Optional[int] = None


class LogininforModel(BaseModel):
    """
    登录日志表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    info_id: Optional[int] = None
    user_name: Optional[str] = None
    ipaddr: Optional[str] = None
    login_location: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None
    status: Optional[str] = None
    msg: Optional[str] = None
    login_time: Optional[datetime] = None


class OperLogQueryModel(OperLogModel):
    """
    操作日志管理不分页查询模型
    """
    oper_time_start: Optional[str]
    oper_time_end: Optional[str]


class OperLogPageObject(OperLogQueryModel):
    """
    操作日志管理分页查询模型
    """
    page_num: int
    page_size: int


class OperLogPageObjectResponse(BaseModel):
    """
    操作日志列表分页查询返回模型
    """
    rows: List[Union[OperLogModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteOperLogModel(BaseModel):
    """
    删除操作日志模型
    """
    oper_ids: str


class ClearOperLogModel(BaseModel):
    """
    清除操作日志模型
    """
    oper_type: str


class LoginLogQueryModel(LogininforModel):
    """
    登录日志管理不分页查询模型
    """
    login_time_start: Optional[str]
    login_time_end: Optional[str]


class LoginLogPageObject(LoginLogQueryModel):
    """
    登录日志管理分页查询模型
    """
    page_num: int
    page_size: int


class LoginLogPageObjectResponse(BaseModel):
    """
    登录日志列表分页查询返回模型
    """
    rows: List[Union[LogininforModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteLoginLogModel(BaseModel):
    """
    删除登录日志模型
    """
    info_ids: str


class ClearLoginLogModel(BaseModel):
    """
    清除登录日志模型
    """
    oper_type: str


class UnlockUser(BaseModel):
    """
    解锁用户模型
    """
    user_name: str


class CrudLogResponse(BaseModel):
    """
    操作各类日志响应模型
    """
    is_success: bool
    message: str
