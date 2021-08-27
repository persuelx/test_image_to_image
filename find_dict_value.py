import json
def read_DataStru_json(path):
    with open(path, 'r', encoding='utf-8') as load_f:
        strF = load_f.read()
        if len(strF) > 0:
            datas = json.loads(strF)
        else:
            datas = {}
    return datas
search = ["box_b"]
def enumerate_fn(data2):
    for index, value in enumerate(data2):
        for key, value in data2[index].items():
            if value in search:
                print(data2[index]["rectangle"])
data2 = read_DataStru_json("./boxes.json")
enumerate_fn(data2["boxes"])