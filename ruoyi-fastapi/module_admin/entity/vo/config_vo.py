from pydantic import BaseModel
from typing import Union, Optional, List


class ConfigModel(BaseModel):
    """
    参数配置表对应pydantic模型
    """
    config_id: Optional[int] = None
    config_name: Optional[str] = None
    config_key: Optional[str] = None
    config_value: Optional[str] = None
    config_type: Optional[str] = None
    create_by: Optional[str] = None
    create_time: Optional[str] = None
    update_by: Optional[str] = None
    update_time: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


class ConfigQueryModel(ConfigModel):
    """
    参数配置管理不分页查询模型
    """
    create_time_start: Optional[str] = None
    create_time_end: Optional[str] = None


class ConfigPageObject(ConfigQueryModel):
    """
    参数配置管理分页查询模型
    """
    page_num: int
    page_size: int


class ConfigPageObjectResponse(BaseModel):
    """
    参数配置管理列表分页查询返回模型
    """
    rows: List[Union[ConfigModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteConfigModel(BaseModel):
    """
    删除参数配置模型
    """
    config_ids: str


class CrudConfigResponse(BaseModel):
    """
    操作参数配置响应模型
    """
    is_success: bool
    message: str
