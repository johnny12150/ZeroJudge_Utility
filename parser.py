import json
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

# 處理預設編碼為utf-8
# with open("a067_uva12149. Feynman.zjson",encoding='utf-8', errors='ignore') as json_data:
#      print(json.load(json_data, strict=False))

problem_id = [272, 458, 10018, 10038, 10789, 10903, 10924, 11059, 11192, 11204, 11219, 11398, 11875, 12289, 12650]

template = { 
    "comment":"",
    "samplecode":"",
    "errmsg_visible":1,
    "problemimages":[ 
 
    ],
    "display":"open",
    "difficulty":0,
    "backgrounds":"[UVa]",
    "keywords":"[]",
    "sortable":"",
    "scores":[ 
       100
    ],
    "timelimits":[ 
       3.0
    ],
    "hint":"",
    "specialjudge_language":{ 
       "suffix":"python",
       "name":"PYTHON"
    },
    "memorylimit":64,
    "theinput":"<p>as pdf</p>",
    "theoutput":"<p>as pdf</p>",
    "testfilelength":1,
    "judgemode":"Strictly",
    "specialjudge_code":"",
    "author":"zero",
    "locale":"zh_TW",
    "language":"C",
 }

def fetch_udebug(problem_id):
    url = "https://udebug.com/UVa/" + str(problem_id)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    # also works
    # soup = BeautifulSoup(res.text, "html.parser")

    # title
    return soup.select('.unflag-problem-title.problem-title')[0].get_text()


# 取得某題在udebug上的測資
def fetch_udebug_api(problem_id):
    user = "你的udebug帳號"
    pwd = "你的udebug密碼"
    # 取得有哪些test input的id
    url = "https://udebug.com/input_api/input_list/retrieve.json"
    payload = {"judge_alias": 'UVa', "problem_id": str(problem_id)}
    res = requests.get(url, params=payload, auth=HTTPBasicAuth(user, pwd)).json()
    if len(res) > 0:
        # 根據input id取test.in
        url2 = "https://www.udebug.com/input_api/input/retrieve.json"
        payload2 = {"input_id": res[0]['id']}
        res_in = requests.get(url2, params=payload2, auth=HTTPBasicAuth(user, pwd)).json()

        # 根據input id取test.out
        url3 = 'https://www.udebug.com/output_api/output/retrieve.json'
        res_out = requests.get(url3, params=payload2, auth=HTTPBasicAuth(user, pwd)).json()
        # 切割\n
        # print(list(filter(None,res_out[0].split('\n'))))
        return res_in, res_out

    else:
        res_in = ''
        res_out = ''

    return res_in, res_out

for i, pid in enumerate(problem_id):
    test_in, test_out = fetch_udebug_api(pid)

    # 模擬一個zjson
    with open("./zjson/"+str(pid)+".zjson", 'w', encoding='utf-8') as json_data:
        src = "http://140.113.87.172/PDF/uva_"+ str(pid) +".pdf"
        uva01 = template
        uva01['reference'] = ""
        uva01['testinfiles'] = test_in
        uva01['testoutfiles'] = test_out
        uva01['title'] = "uva."+ str(pid) + " " +fetch_udebug(pid)
        uva01['sampleinput'] = ""
        uva01['sampleoutput'] = ""
        uva01['content'] = "<p><embed src=\"" + src + "\" type=\"application/pdf\" width=\"700\" height=\"700\"></embed></p>"
        json.dump(uva01, json_data)

