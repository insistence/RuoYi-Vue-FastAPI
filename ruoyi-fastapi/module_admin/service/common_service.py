from fastapi import Request
import os
from fastapi import UploadFile
from datetime import datetime
from config.env import UploadConfig
from module_admin.entity.vo.common_vo import *
from utils.upload_util import UploadUtil


class CommonService:
    """
    通用模块服务层
    """

    @classmethod
    def upload_service(cls, request: Request, file: UploadFile):
        if not UploadUtil.check_file_extension(file):
            return False
        relative_path = f'upload/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass
        filename = f'{file.filename.rsplit(".", 1)[0]}_{datetime.now().strftime("%Y%m%d%H%M%S")}{UploadConfig.UPLOAD_MACHINE}{UploadUtil.generate_random_number()}.{file.filename.rsplit(".")[-1]}'
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'wb') as f:
            # 流式写出大型文件，这里的10代表10MB
            for chunk in iter(lambda: file.file.read(1024 * 1024 * 10), b''):
                f.write(chunk)

        result = UploadResponseModel(
            fileName=f'{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{filename}',
            newFileName=filename,
            originalFilename=file.filename,
            url=f'{request.base_url}{UploadConfig.UPLOAD_PREFIX[1:]}/{relative_path}/{filename}'
        )

        return result

    @classmethod
    def delete_download_file_services(cls, filepath: str):
        """
        文件下载完成后删除对应文件
        """
        os.remove(filepath)

