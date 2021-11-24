# 写入xls文件
import datetime

import xlrd
import xlwt
from xlutils.copy import copy


def write_excel_xls_append(path, value):
    index = len(value)                                           # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path, formatting_info=True)    # 打开工作簿
    worksheet = workbook.sheet_by_name('oracle巡检')              # 获取工作簿中的oracle巡检表格
    rows_old = worksheet.nrows                                   # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)                                # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)                    # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        new_worksheet.write(rows_old,i, value[i], set_style())    # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)                                                   # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


def set_style():
    style = xlwt.XFStyle()              # 初始化样式
    font = xlwt.Font()                  # 为样式创建字体
    al = xlwt.Alignment()
    al.horz = 0x02                      # 设置水平居中
    al.vert = 0x01                      # 设置垂直居中
    style.alignment = al
    font.name = 'Times New Roman'
    font.bold = 200
    font.height = 20 * 10
    font.color_index = 4
    style.font = font
    return style


def merge(path):               ## 生成巡检报告
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'oracle巡检', cell_overwrite_ok=True)  # 创建sheet
    #row0 = ["数据库名", "数据库状态", "表空间>85%", "asm使用率>85%", "数据文件状态", "dbtime", "备份检查"]
    #row1 = ["参数", "当前值", "历史值", "最大值", "用户名", "用户状态","密码过期"]
    ## 生成第一行
    #for i in range(0, len(row0)):
    #    sheet1.write_merge(0, 1, i, i, row0[i], set_style())
    #sheet1.write_merge(0, 0, 7, 10, 'session', set_style())
    #sheet1.write_merge(0, 0, 11, 13, '用户', set_style())
    #for i in range(0, len(row1)):
    #    sheet1.write(1, i + 7, row1[i], set_style())

    row0 = ["数据库名", "数据库状态", "表空间>85%", "asm使用率>85%", "数据文件状态"]
    row1 = ["参数", "当前值", "历史值", "最大值", "用户名", "用户状态","密码过期"]
    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write_merge(0, 1, i, i, row0[i], set_style())
    sheet1.write_merge(0, 0, 5, 8, 'session', set_style())
    sheet1.write_merge(0, 0, 9, 11, '用户', set_style())
    sheet1.write_merge(0, 1, 12, 12, 'dbtime', set_style())
    sheet1.write_merge(0, 1, 13,13, '备份检查', set_style())
    for i in range(0, len(row1)):
        sheet1.write(1, i + 5, row1[i], set_style())


    sheet1.col(0).width = 3000
    sheet1.col(1).width = 3500
    sheet1.col(2).width = 5000
    sheet1.col(3).width = 3000
    sheet1.col(4).width = 3500
    sheet1.col(5).width = 3000
    sheet1.col(6).width = 3000
    sheet1.col(7).width = 2000
    sheet1.col(8).width = 2000
    sheet1.col(9).width = 5000
    sheet1.col(10).width = 5000
    sheet1.col(11).width = 5500
    sheet1.col(12).width = 15000
    sheet1.col(13).width = 30000

    f.save(path)  # 保存文件


# 测试如下：
#time = datetime.datetime.now().strftime('%Y%m%d_%H%M')
#workbook = "数据库每日检查报告_%s.xls" % time
#merge(workbook)                            ## 生成巡检报告
#value=[['交易系统1','paydb1','OPEN','1232131231243213123------------123213421312321312\n1231231214r234','5','6','7','8','9'],
#       ['交易系统2','paydb2','close','4','5','6','7','8','9'],
#       ['交易系统3','paydb3','mount','4','5','6','7','8','9']]
#write_excel_xls_append(workbook, value)
