import json
import requests
import bupt_auth


try:
    with open("auth.json", "r") as file:
        account_data = json.load(file)
        tenant_id = account_data["tenant_id"]
        user_id = account_data["user_id"]
        auth_token = account_data["auth_token"]
        blade = account_data["blade"]
except FileNotFoundError:
    account = input("请输入学号：")
    password = input("请输入密码：")
    bupt_auth.get_co_and_sa(account, password)

    with open("auth.json", "r") as file:
        account_data = json.load(file)
        tenant_id = account_data["tenant_id"]
        user_id = account_data["user_id"]
        auth_token = account_data["auth_token"]
        blade = account_data["blade"]

ucloud_api_url = "https://apiucloud.bupt.edu.cn"
ucloud_course_file_url = "https://fileucloud.bupt.edu.cn/ucloud/document/"
ucloud_assignment_file_url = "https://apiucloud.bupt.edu.cn/blade-source/resource/filePath"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "application/json, text/plain, */*",
    "Authorization": auth_token,
    "Tenant-Id": tenant_id,
    "Blade-Auth": blade,
}


def get_courses():
    params = {
        "userId": user_id,
        "size": 999999,
        "current": 1,
    }

    response = requests.get(
        ucloud_api_url + "/ykt-site/site/list/student/current",
        headers=headers,
        params=params,
    )
    data = response.json()["data"]
    records = data["records"]

    for record in records:
        print(
            "课程名称: ",
            record["siteName"],
            "课程ID: ",
            record["id"],
        )


def get_course_detail(course_id):
    params = {
        "id": course_id,
    }

    response = requests.get(
        ucloud_api_url + "/ykt-site/site/detail", headers=headers, params=params
    )
    print(response.json()["data"])


def get_course_files(course_id):
    params = {
        "siteId": course_id,
        "userId": user_id,
    }

    response = requests.post(
        ucloud_api_url + "/ykt-site/site-resource/tree/student",
        headers=headers,
        params=params,
    )

    resources = [
        attachment["resource"]
        for record in response.json()["data"]
        for attachment in record.get("attachmentVOs", [])
    ] + [
        attachment["resource"]
        for record in response.json()["data"]
        for child in record.get("children", [])
        for attachment in child.get("attachmentVOs", [])
    ]

    for resource in resources:
        print(resource["name"], resource["storageId"], resource["ext"])


def get_assignments(course_id):
    body = {
        "userId": user_id,
        "siteId": course_id,
    }

    response = requests.post(
        ucloud_api_url + "/ykt-site/work/student/list", headers=headers, json=body
    )
    for record in response.json()["data"]["records"]:
        print(record)


def get_assignment_detail(assignment_id):
    params = {
        "assignmentId": assignment_id,
    }

    response = requests.get(
        ucloud_api_url + "/ykt-site/work/detail", headers=headers, params=params
    )
    data = response.json()["data"]

    print(data["assignmentTitle"], "\n", data["assignmentContent"])

    if data["assignmentResource"] == []:
        pass
    else:
        print("Assignment Resource:")
        for i in data["assignmentResource"]:
            print(i["resourceId"], i["resourceName"], i["resourceType"])


def get_todo_list():
    params = {
        "userId": user_id,
    }

    response = requests.get(
        ucloud_api_url + "/ykt-site/site/student/undone", headers=headers, params=params
    )

    for record in response.json()["data"]["undoneList"]:
        print(record)


def download_course_file(file_name, storage_id, file_format):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
    }

    response = requests.get(
        ucloud_course_file_url + storage_id + "." + file_format, headers=headers
    )
    with open(file_name, "wb") as file:
        file.write(response.content)

def download_assignment_file(filename, resourceId):
    params = {
        "resourceId": resourceId
    }
    res = requests.get(ucloud_assignment_file_url, params=params, headers=headers)

    print(res.text)
    file_url = res.json()["data"]
    print(file_url)

    response = requests.get(file_url)

    with open(filename, "wb") as file:
        file.write(response.content)