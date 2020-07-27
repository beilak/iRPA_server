import requests
import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def get_token(rpa):
    """ Get token from RPA server
   :return: token string
   """
    token = {'access_token': ''}
    if (rpa['type'] == 'RPA_SAP_IRPA'):
        OAUTH_URL = ""
        CLIENT_ID = "00000000"
        CLIENT_SECRET = "0000000000000"
        client = BackendApplicationClient(client_id=CLIENT_ID)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=OAUTH_URL, client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET)

    return token


def get_RPA_request(rpa, token):
    """
   Get data for RPA task (from request)
   :return: url is request URL, payload data for request
   """
    http_req_type = rpa['http']
    url = rpa['url']
    body = rpa['body']
    headers = {
        'Content-Type': 'application/json'
    }

    header = rpa['header']
    headers.update(header)

    try:
        access_token = token['access_token']
    except:
        access_token = ''
    if access_token != '':
        access_token = {'Authorization': 'Bearer ' + token['access_token']}
        headers.update(access_token)

    return url, headers, body


def do_RPA_task(token, url, header, body):
    """
   Send request to RPA server
   :param token: token for RPA server
   :param url: Request URL
   :param payload: data for request
   :return:
   """

    # TODO add header to headers
    body = json.dumps(body)
    response = requests.request("POST", url, headers=header, data=body)
    is_task_response = False
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        is_task_response = True
    return response, is_task_response


def get_rpa_tasks(payload):
    rpa_list = payload['custom']['rpa']['list']
    return rpa_list


def iRPA(request):
    """
   Run RPA service
   :param request: request from WEB
   :return: returne result
   """
    data = request.json
    fulfillmentMessages = data['queryResult']['fulfillmentMessages']
    for flm in fulfillmentMessages:
        try:
            payload = flm['payload']
        except:
            pass
    # payload = [0]['payload']
    rpa_list = get_rpa_tasks(payload)
    result_json = ""
    for rpa in rpa_list:
        token = get_token(rpa)
        url, header, body = get_RPA_request(rpa, token)
        rpa_result, is_task_response = do_RPA_task(token, url, header, body)
        try:
            if is_task_response:
                result_json += result_json + rpa["success_text"] + "\n"
        except:
            pass
        '''
        try:
            rpa_result_txt = json.loads(rpa_result.text.encode('utf8'))
        except:
            rpa_result_txt = ''
        result_json.update({'result of ' + rpa['type'] : rpa_result_txt})
        '''
    # result_json = { "text": { "text": [ "my text" ] } }
    responseId = data["responseId"]
    result_json = json.dumps({
        'fulfillmentText': result_json
    })

    return result_json
