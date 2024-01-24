import random
from fastapi import UploadFile
from config.env import UploadConfig


class UploadUtil:
    """
    上传工具类
    """

    @classmethod
    def generate_random_number(cls):
        """
        生成3位数字构成的字符串
        """
        random_number = random.randint(1, 999)

        return f'{random_number:03}'

    @classmethod
    def check_file_extension(cls, file: UploadFile):
        """
        检查文件后缀是否合法
        """
        file_extension = file.filename.rsplit('.')[-1]
        if file_extension in UploadConfig.DEFAULT_ALLOWED_EXTENSION:
            return True
        return False

    @classmethod
    def check_file_machine(cls, filename):
        """
        校验文件机器码是否合法
        """
        if filename.rsplit('.', 1)[-4] == UploadConfig.UPLOAD_MACHINE:
            return True
        return False

    @classmethod
    def check_file_random_code(cls, filename):
        """
        校验文件随机码是否合法
        """
        valid_code_list = [f"{i:03}" for i in range(1, 999)]
        if filename.rsplit('.', 1)[-1:-4] in valid_code_list:
            return True
        return False
