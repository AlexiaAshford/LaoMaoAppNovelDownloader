import sys
import time
import requests
from API.AesDecrypt import decrypt, example
from API import UrlConstants

headers = {
    "Host": "api.laomaoxs.com",
    "Keep-Alive": "300",
    "Connection": "Keep-Alive",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}


def get(url, params=None, retry=10, **kwargs):
    api_url = UrlConstants.WEB_SITE + url.replace(UrlConstants.WEB_SITE, '')
    for count in range(retry):
        try:
            return example(decrypt(str(requests.get(api_url, params=params, headers=headers, **kwargs).text)))
        except (OSError, TimeoutError, IOError) as e:
            if retry != retry - 1:
                print("\nGet Error Retry: " + str(e) + '\n' + api_url)
                time.sleep(1 * count)
            else:
                print("\nGet Failed: " + str(e) + '\n' + api_url)
                sys.exit(1)



def post(url, data=None, retry=10, **kwargs):
    api_url = UrlConstants.WEB_SITE + url.replace(UrlConstants.WEB_SITE, '')
    for count in range(retry):
        try:
            return example(decrypt(str(requests.post(api_url, data, headers=headers, **kwargs).text)))
        except (OSError, TimeoutError, IOError) as e:
            if retry != retry - 1:
                print("\nGet Error Retry: " + str(e) + '\n' + api_url)
                time.sleep(1 * count)
            else:
                print("\nPost Failed: " + str(e) + '\n' + api_url + "\nTerminating......")
                sys.exit(1)