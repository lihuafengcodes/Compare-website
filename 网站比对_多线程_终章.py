import requests
import difflib
import time
import random
from multiprocessing import Pool

# filename = input("请输入包含Url的Txt文件名：")
url_list = list()
with open("urls.txt") as f:  # 读取txt文件获得url列表
    for url_result in f.readlines():
        url_list.append("http://" + url_result.strip('\n').strip('.'))  # 去除换行符
# print(url_list)
false_header = {
    'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
true_header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'}


def true_html(target_url, header):  # 获取正确的界面内容
    true_response = requests.get(
        target_url, headers=header)
    if true_response.status_code == 200:
        return true_response.text


def false_html(target_url, headers):  # 伪装成百度爬虫获取页面内容
    false_response = requests.get(
        target_url, headers=headers)
    if false_response.status_code == 200:
        return false_response.text


def main(url, true_headers, false_headers):
    error = list()
    Connect_error_urls = list()
    print("正在比对:" + url + "." * 8)
    try:
        true = true_html(url, true_headers)
        false = false_html(url, false_headers)
        ratio = difflib.SequenceMatcher(None, false, true).quick_ratio()
        if ratio < 1:
            error.append(str(ratio) + "*" * 8 + url)
            print('抓取到一个疑似错误' + str(ratio) + "*" * 8 + url)
    except requests.exceptions.ConnectionError:
        Connect_error_urls.append(url)
        sleep_time = random.randint(1, 7)
        time.sleep(sleep_time)
        print('.' * 8 + '战术休眠 %s s' +'.' * 8 % sleep_time)
        pass

    for result in error:  # 写入文本
        with open("re.txt", "a+") as g:
            g.write(result + "\n")
    for Connect_error_url in Connect_error_urls:  # 写入文本
        with open("Connect_error_urls.txt", "a+") as g:
            g.write(Connect_error_urls + "\n")


if __name__ == '__main__':
    po = Pool(3)
    for url in url_list:
        Error_url = po.apply_async(main, (url, true_header, false_header,))

    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接收新的请求
    po.join()  # 等待po中所有子进程执行完成，必须放在close语句之后
    print("-----end-----")
