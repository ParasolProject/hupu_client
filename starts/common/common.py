CODE_SUCCESS = "100"
CODE_UNAVAILABLE = "101"


def liz_rest_response(code=CODE_SUCCESS, msg='', data=None):
    rs = {
            'resultCode': code,
            'detailDescription': msg,
            'resultContent': None,
            'pageInfo': {},
        }
    if data is not None:
        rs['resultContent'] = data
    return rs


def patch_response(resp, code=CODE_SUCCESS):
    resp.data = liz_rest_response(msg='', code=code, data=resp.data)
    return resp



