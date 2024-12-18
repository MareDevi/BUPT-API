import requests
import bupt_auth

account = input("请输入学号：")
password = input("请输入密码：")

api_url = "https://apiucloud.bupt.edu.cn"

account_data = bupt_auth.get_co_and_sa(account, password)

user_id = account_data[1]
auth_token = account_data[2]
blade = account_data[3]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "application/json, text/plain, */*",
    "Authorization": auth_token,
    "Tenant-Id": "000000",
    "Blade-Auth": blade,
}

def get_courses():

    params = {
    "userId": user_id,
    }
    
    response = requests.get(api_url + "/ykt-site/site/list/student/current", headers=headers, params=params)
    data = response.json()["data"]
    records = data["records"]
    
    for record in records:
        print(record)

def get_course_detail(course_id):
    
    params = {
    "id": course_id,
    }
    
    response = requests.get(api_url + "/ykt-site/site/detail", headers=headers, params=params)
    print(response.json()["data"])

def get_course_files(course_id):
    
    params = {
    "siteId": course_id,
    "userId": user_id,
    }
    
    response = requests.post(api_url + "/ykt-site/site-resource/tree/student", headers=headers, params=params)

    for record in response.json()["data"]:
        if record["children"] == []:
            pass
        else:
            for i in record["children"]:
                        if i["attachmentVOs"] == []:
                            pass
                        else:
                            for each in i["attachmentVOs"]:
                                print(each["resource"])
        if record["attachmentVOs"] == []:
            pass
        else:
            for each in record["attachmentVOs"]:
                print(each["resource"])

def get_assignments(course_id):
    
    body = {
    "userId": user_id,
    "siteId": course_id,
    }
    
    response = requests.post(api_url + "/ykt-site/work/student/list", headers=headers, json=body)
    for record in response.json()["data"]["records"]:
        print(record)

def get_assignment_detail(assignment_id):
    
    params = {
    "assignmentId": assignment_id,
    }

    response = requests.get(api_url + "/ykt-site/work/detail", headers=headers, params=params)

    print(response.json()['data'])

def get_todo_list():
    
    params = {
    "userId": user_id,
    }
    
    response = requests.get(api_url + "/ykt-site/site/student/undone", headers=headers, params=params)

    for record in response.json()["data"]["undoneList"]:
        print(record)