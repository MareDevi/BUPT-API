import requests

account = input("请输入账号：")
password = input("请输入密码：")

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Accept-Language": "en-US,en;q=0.5",
	"Connection": "keep-alive",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"
}

auth_url = "https://jwgl.bupt.edu.cn//Logon.do?method=logon&flag=sess"
login_url = "https://jwgl.bupt.edu.cn/Logon.do?method=logon"

data = {
        "userAccount": account,
        "userPassword": password
        }

response = requests.post(auth_url, data=data, headers=headers)

cookie = response.cookies
datastr = response.text

scode = datastr.split("#")[0]
sxh = datastr.split("#")[1]
code = f"{account}%%%{password}"
encoded = ""

for i in range(len(code)):
    if i < 20:
        encoded += code[i] + scode[:int(sxh[i])]
        scode = scode[int(sxh[i]):]
    else:
        encoded += code[i:]
        break

data = {
        "userAccount": account,
        "userPassword": password,
        "encoded": encoded
        }

response = requests.post(login_url, data=data, headers=headers, cookies=cookie)

print(response.text)