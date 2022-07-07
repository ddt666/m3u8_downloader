import requests
import time

resp = requests.get(
    "https://s-file-1.ykt.cbern.com.cn/zxx/s_course/v2/activity_sets/b6a9c903-f14e-4aca-9939-57475ee375e4/fulls.json")
if resp.status_code == 200:

    nodes = resp.json().get("nodes")
    videos = {}
    for node in nodes:

        node_name = node.get("node_name").strip()
        childs = node.get("child_nodes")
        for child in childs:
            child_name = child.get("node_name")
            child_id = child.get("node_id")
            detail_url = f"https://s-file-1.ykt.cbern.com.cn/zxx/s_course/v1/x_class_hour_activity/{child_id}/resources.json"
            videos.update({f"({node_name}){child_name}".format(node_name=node_name, child_name=child_name): detail_url})
            # break
    m3u8_d = {}
    for n, u in videos.items():
        resp = requests.get(u)
        if resp.status_code == 200:
            detail = resp.json()
            m3u8_url = detail[0].get("video_extend").get("urls")[2].get("urls")[0]
            print(m3u8_url)
            m3u8_d.update({n: m3u8_url})
        time.sleep(2)
    print(m3u8_d)
    with open("人教数学三年级上册.txt", "a+", encoding="utf8")  as f:

        for n, m in m3u8_d.items():
            f.write(n + "|" + m+"\n")
    print("抓取完毕")
