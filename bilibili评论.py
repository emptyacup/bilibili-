mport json
import re
import urllib.request,urllib.error
import time
import xlwt

            #三个josn链接，找规律
"""                                      --------------------------------------------------删了
https://api.bilibili.com/x/v2/reply/main?callback=jQuery172014529710084556746_1649311888399&jsonp=jsonp&next=0&type=1&oid=500865249&mode=3&plat=1&_=1649311897893
https://api.bilibili.com/x/v2/reply/main?callback=jQuery172014529710084556746_1649311888402&jsonp=jsonp&next=2&type=1&oid=500865249&mode=3&plat=1&_=1649312232203
https://api.bilibili.com/x/v2/reply/main?callback=jQuery172014529710084556746_1649311888405&jsonp=jsonp&next=3&type=1&oid=500865249&mode=3&plat=1&_=1649313371129
"""


def main():

     #网站链接
    url1="https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next="
    url2='&type=1&oid=500865249&mode=3&plat=1'
    # url=url1+'1'+url2
    savepath='评论.xls'


    html=[]
    for i in range(1,8):
        respose=[]
        url=url1+str(i)+url2
        # print(url)
        respose=ask(url)        #获取页面消息
        html.append(respose)

        time.sleep(10)

    datalist=request_data(html)           #解析分类消息
    save_data(datalist, savepath)           #保存信息






    # html=ask(url)


    # respnse=open('comment.html','r',encoding='utf-8')
    # html=str(respnse.read())





def request_data(html):


    datalist=[]
    for html_apart in html:

        list=json.loads(html_apart)
        replies=list["data"]["replies"]

        for item in replies:
            if not item["member"]["sign"]:
                item["member"]["sign"]="肿个人木有个性标签"
            if not item["member"]["vip"]["label"]["text"]:
                item["member"]["vip"]["label"]["text"]="现在还不是0.0"
            data=[]
            data.append(item["member"]["uname"])
            data.append(item["member"]["sign"])
            data.append(item["member"]["sex"])
            data.append(item["content"]["message"])
            data.append(item["member"]["avatar"])
            data.append(item["member"]["level_info"]["current_level"])
            data.append(item["member"]["vip"]["label"]["text"])
            data.append(item["reply_control"]["time_desc"])

            datalist.append(data)
            #print("用户名:"+item["member"]["uname"]+"      个性名称："+item["member"]["sign"]+"      性别："+item["member"]["sex"]+"      消息内容："+item["content"]["message"]+"      头像："+item["member"]["avatar"])



    # print(datalist)

    return datalist


def save_data(datalist,savepath):
    book=xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet=book.add_sheet('评论消息',cell_overwrite_ok=True)
    col=('用户名','个性签名','性别','消息','用户头像','等级','vip','距离现在时间')
    a=0
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for data in datalist:
        a+=1
        for i in range(0,8):
            sheet.write(a,i,data[i])
    book.save(savepath)





def ask(url):
    head = {
        "referer":"https://www.bilibili.com/video/BV1BK411g7Pm?spm_id_from=333.999.0.0",
        "User-Agent": ""
    }
    html=""

    request = urllib.request.Request(url, headers=head)

    try:


        response=urllib.request.urlopen(request)

        html=response.read().decode('utf-8')


    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html





if __name__ == '__main__':
    main()
