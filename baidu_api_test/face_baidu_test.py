import copy
from baidubce import bce_base_client
from baidubce.auth import bce_credentials
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import bce_client_configuration


# 人脸检测 Python示例代码
class ApiCenterClient(bce_base_client.BceBaseClient):

    def __init__(self, config=None):
        self.service_id = 'apiexplorer'
        self.region_supported = True
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)

        if config is not None:
            self.config.merge_non_none_values(config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    def demo(self):
        path = b'/rest/2.0/face/v3/detect'
        headers = {}
        headers[b'Content-Type'] = 'application/json;charset=UTF-8'

        params = {}

        body = '{\"image\":\"https:\/\/baidu-ai.bj.bcebos.com\/face\/faces.jpg\",\"image_type\":\"URL\"}'
        return self._send_request(http_methods.POST, path, body, headers, params)


if __name__ == '__main__':
    endpoint = 'https://aip.baidubce.com'
    ak = 'Tho0GSuXexrR5awGRKIWRpMC'
    sk = 'xGBPRNMaZDG4IOXHhWDt3axrRiCYiR80'
    config = bce_client_configuration.BceClientConfiguration(credentials=bce_credentials.BceCredentials(ak, sk),
                                                             endpoint=endpoint)
    client = ApiCenterClient(config)
    res = client.demo()
    print(res.__dict__['raw_data'])
