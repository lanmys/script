# 读取台账

import cx_Oracle
import xlrd
import sql
import data_deal


def read_oracle_list(oracle_list_file):
        readbook = xlrd.open_workbook(oracle_list_file, formatting_info=True)
        worksheet = readbook.sheets()[0]
        oracle_list = []
        for i in range(1, worksheet.nrows):
            list = worksheet.row_values(i)
            oracle_list.append(list)
        return oracle_list


def conn_oracle(ora_list):
    db_ip = ora_list[3]
    db_port = ora_list[4]
    db_inst = ora_list[7]
    db_user = ora_list[5]
    passwd = ora_list[6]
    oracle_url = '{}:{}/{}'.format(db_ip, db_port, db_inst)
    try:
        conn = cx_Oracle.connect(db_user, passwd, oracle_url)
        return conn
    except Exception as e:
        print('IP:{},oracle connect error:{}'.format(db_ip,e))



def get_data(conn,ispdb):
    curs = conn.cursor()
    ispdb = ispdb

    ## dbname
    sql_dbname = sql.sql_dbname(ispdb)
    curs.execute(sql_dbname)
    dbname = data_deal.deal_dbname(curs)

    ## open_mode
    curs.execute(sql.sql_open_mode)
    open_mode = data_deal.deal_dbname(curs)

    ## tablesapce
    curs.execute(sql.sql_tablespace)
    tablespace = data_deal.deal_tablespace(curs)

    curs.execute(sql.sql_asm)
    asm = data_deal.deal_asm(curs)

    curs.execute(sql.sql_datafile)
    datafile = data_deal.deal_datafile(curs)

    curs.execute(sql.sql_dbtime)
    dbtime = data_deal.deal_dbtime(curs)

    curs.execute(sql.sql_rman)
    rman_backup = data_deal.deal_rman(curs)

    curs.execute(sql.sql_session)
    session = data_deal.deal_session(curs)

    curs.execute(sql.sql_users)
    user_info = data_deal.deal_user(curs)

    curs.close()
    conn.close()

    result = [dbname, open_mode, tablespace, asm, datafile, session[0],session[1],session[2],
              session[3],user_info['username'],user_info['status'],user_info['expired'],dbtime,rman_backup]
    return result




#oracle_list = read_oracle_list('oracle_list1.xls')
#for i in oracle_list:
#    conn = conn_oracle(i)
#    curs = conn.cursor()
#    sql = 'select SUBSTR (VERSION,0,2) version from v$instance'
#    curs.execute(sql)
#    for result in curs:
#        print(result)
#curs.close()
#conn.close()