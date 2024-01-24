from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends, File, Form, Query
from sqlalchemy.orm import Session
from config.env import CachePathConfig, UploadConfig
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_admin.service.common_service import *
from module_admin.service.config_service import ConfigService
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from typing import Optional

commonController = APIRouter(prefix='/common')


@commonController.post("/upload")
async def common_upload(request: Request, file: UploadFile = File(...)):
    try:
        upload_result = CommonService.upload_service(request, file)
        logger.info('上传成功')
        return ResponseUtil.success(model_content=upload_result)
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=str(e))


@commonController.get("/download")
async def common_download(request: Request, background_tasks: BackgroundTasks, file_name: str = Query(alias='fileName'), delete: bool = Query()):
    try:
        def generate_file(path):
            with open(path, 'rb') as response_file:
                yield from response_file

        filepath = os.path.join(file_name.replace(UploadConfig.UPLOAD_PREFIX, UploadConfig.UPLOAD_PATH))
        result = generate_file(filepath)
        if delete:
            background_tasks.add_task(CommonService.delete_download_file_services, filepath)
        return ResponseUtil.streaming(data=result)
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=str(e))


@commonController.get("/config/query/{config_key}")
async def query_system_config(request: Request, config_key: str):
    try:
        # 获取全量数据
        config_query_result = await ConfigService.query_config_list_from_cache_services(request.app.state.redis,
                                                                                        config_key)
        logger.info('获取成功')
        return response_200(data=config_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
