'''
抓取拉钩数据
'''
import requests
import xlwt
import time

base_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

def get_lagou(keyword, page_count):
    lagou_list = []
    for i in range(page_count):

        Myheaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Referer': 'https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput='
            }

        time.sleep(5)
        session = requests.session()  # 获取session
        session.headers.update(Myheaders) # 更新header信息，cookies会变
        session.get("https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=")

        try:
            from_data = {
                'first': 'false',
                'pn': str(i+1),
                'kd': keyword
            }

            print('正在爬取第%s职位的%s页' %(keyword, str(i+1)))

            response = session.post(base_url, headers=Myheaders, data= from_data)
            response.encoding = 'utf-8'
            info_list = response.json()['content']['positionResult']['result']
            companyIds_list = []
            for job in info_list:
                information = []
                information.append(keyword)  # 岗位对应ID
                information.append(job['city'])  # 岗位对应城市
                information.append(job['companyFullName'])  # 公司名
                information.append(job['companySize'])  # 公司规模
                information.append(job['companyLabelList'])  # 福利待遇
                information.append(job['district'])  # 工作地点
                information.append(job['education'])  # 学历要求
                information.append(job['firstType'])  # 工作类型
                information.append(job['positionName'])  # 职位名称
                information.append(job['salary'])  # 薪资
                information.append(job['workYear'])  # 工作年限
                information.append(job['financeStage'])  # 公司发展阶段
                information.append(job['skillLables'])  # 技能要求
                lagou_list.append(information)
                companyIds_list.append(job['companyId'])


        except Exception as e:
            print('程序出错',e)
        continue

    return lagou_list

def main():
    info_result = []
    title = ['职位类型','城市','公司名','公司规模','福利待遇', '工作地点', '学历要求', '工作类型', '职位名称', '薪资', '工作年限','公司发展阶段','技能要求']
    info_result.append(title)

    #抓取数据分析语言信息
    lagou_list_chanpin = get_lagou('数据分析',50)

    # 抓取php语言信息
    lagou_list_yunying = get_lagou('php', 50)


    info_result.extend(lagou_list_chanpin)
    info_result.extend(lagou_list_yunying)


    # 创建workbook,即excel
    workbook = xlwt.Workbook(encoding='utf_8_sig')
    # 创建表,第二参数用于确认同一个cell单元是否可以重设值
    worksheet = workbook.add_sheet('lagou', cell_overwrite_ok=True)
    for i, row in enumerate(info_result):
        for j, col in enumerate(row):
            worksheet.write(i, j, col)
    workbook.save('lagou.xls')


if __name__ == '__main__':
    main()