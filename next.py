"""
这里写的是登录逻辑
"""

import re, os, random, qrcode, requests, subprocess

uuid = ""
code = ""
token = ""


def generate_android_id():
    """生成AndroidId"""
    return (
        "".join(random.choices("0123456789", k=4))
        + "".join(random.choices("0123456789", k=2))
        + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
        + "".join(random.choices("0123456789", k=4))
        + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
        + "".join(random.choices("0123456789", k=2))
    )


def make_login_qr():
    global uuid, code
    code = ""
    url = "https://open.weixin.qq.com/connect/app/qrconnect?appid=wx0d65adfcbfe55d70&bundleid=cn.lwpro.admin&scope=snsapi_userinfo&state=wechat_sdk_demo_test&supportcontentfromwx=8191"

    # 获取uuid
    r = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.0(0x17000024) NetType/WIFI Language/zh_CN",
        },
    ).text

    uuid = re.search(r'uuid:\s*"(\w+)"', r).group(1)
    print("uuid:", uuid)
    realQrUrl = f"https://open.weixin.qq.com/connect/confirm?uuid={uuid}"

    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(realQrUrl)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="#f0f0f0")
    img.save("qr.gif")


def check_login():
    if uuid:
        try:
            r = requests.get(
                url=f"https://long.open.weixin.qq.com/connect/l/qrconnect?uuid={uuid}",
            ).text
            code = re.search(r"wx_code=\s*'(\w+)'", r).group(1)
            print("code:", code)
            perform_login(code)
        except:
            check_login()


def perform_login(auth_code):
    """登录并获取token"""
    try:
        response = requests.post(
            url="https://block-api.lucklyworld.com/api/auth/wx?uid=&version=4.4.2",
            headers={
                "Accept": "*/*",
                "Accept-Language": "zh-cn",
                "AndroidId": generate_android_id(),
                "Channel": "90585",
                "Connection": "Keep-Alive",
                "Content-Type": "application/x-www-form-urlencoded; Charset=UTF-8",
                "User-Agent": "com.caike.union/4.0.5-90585 Dalvik/2.1.0 (Linux; U; Android 12; 2206123SC Build/V417IR)",
                "Version": "4.4.2",
            },
            data={"credential": auth_code},
        )

        login_data = response.json()
        token = login_data.get("token", "")
        if token:
            print("token:", token)
            clip_board_copy(token)
            with open("token.txt", "w") as f:
                f.write(token)
        return login_data
    except Exception as e:
        print(f"登录失败: {e}")
        return None


def is_token_valid():
    """检查token是否有效"""
    global token
    try:
        with open("token.txt", "r") as f:
            token = f.read()
            print("token:", token)
            r = requests.post(
                url="https://block-api.lucklyworld.com/api/user/info",
                headers={
                    "User-Agent": "com.caike.union/4.4.2-90585 Dalvik/2.1.0 (Linux; U; Android 14; 2211133C Build/UKQ1.230804.001)",
                    "token": token,
                },
            ).json()["nickname"]
            clip_board_copy(token)
        return f"登录成功,欢迎 {r} !"
    except:
        return "未登录或登录失效"


def clip_board_copy(text):
    """复制到剪贴板"""
    command = f"echo {text} | clip"
    subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
