# 测试数据库是否连接成功并返回值
import datetime
import action
import write_check_xls

# 创建报告
time = datetime.datetime.now().strftime('%Y%m%d_%H%M')
workbook = "数据库每日检查报告_%s.xls" % time
write_check_xls.merge(workbook)


def main():
    oracle_list = action.read_oracle_list('oracle_list1.xls')
    for i in oracle_list:
        pdb = i[2]
        try:
            conn = action.conn_oracle(i)
            result = action.get_data(conn, pdb)
            write_check_xls.write_excel_xls_append(workbook, result)
        except:
            if i[2] == 'N':
                warming = 'IP:{},监听程序异常或未启动该实例:{}'.format(i[3], i[7])
                value = [warming]
                write_check_xls.write_excel_xls_append(workbook, value)
            else:
                warming = 'IP:{},监听程序异常或未启动该pdb:{}'.format(i[3], i[7])
                value = [warming]
                write_check_xls.write_excel_xls_append(workbook, value)

        """
        # 测试，勿删
        #conn = action.conn_oracle(i)
        #result = action.get_data(conn,pdb)
        #write_check_xls.write_excel_xls_append(workbook,result)
        """


if __name__ == '__main__':
    main()
