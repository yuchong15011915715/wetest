import configparser
import os


class Config(object):

    # Config方法的初始化
    def __init__(self, config_name=None):
        file_path = os.path.join(os.path.dirname(__file__), config_name)
        # print(str(file_path))
        self.config = configparser.ConfigParser()
        self.config.read(file_path)

    # 获取配置文件中的标头[dbMysql]  configparser解析
    def get_sections(self):
        return self.config.sections()

    # 获取配置文件中的 key
    def get_options(self, section):
        return self.config.options(section)

    # 获取配置文件中的value 根据key
    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.config.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result

