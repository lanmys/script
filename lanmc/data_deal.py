## 数据处理
import cx_Oracle

from lanmc import sql

spacing = '  '

def deal_dbname(curs):
    dbname = ''
    for i in curs:
        dbname = i[0]
    return dbname


def deal_open_mode(curs):
    open_mode = ''
    for i in curs:
        open_mode = i[0]
    return open_mode


def deal_tablespace(curs):
    tablespace = ''
    for i in curs:
        for j in i:
            tablespace = tablespace + spacing + str(j)
        tablespace = tablespace + '\n'
    if tablespace.strip() == '':
        tablespace = '无'
    return tablespace


def deal_asm(curs):
    asm = ''
    for i in curs:
        for j in i:
            asm = asm + spacing + str(j)
        asm = asm + '\n'
    if asm.strip() == '':
        asm = '无'
    return asm

def deal_datafile(curs):
    datafile = ''
    for i in curs:
        for j in i:
            datafile = datafile + spacing + str(j)
        datafile = datafile + '\n'

    if datafile.strip() == '':
        datafile = '无'
    return  datafile


def deal_dbtime(curs):
    dbtime = ''
    for i in curs:
        for j in i:
            dbtime = dbtime + spacing + str(j)
        dbtime = dbtime + '\n'
    return dbtime


def deal_rman(curs):
    rman_backup = ''
    for i in curs:
        for j in i:
            rman_backup = rman_backup + spacing +str(j)
        rman_backup = rman_backup + '\n'

    if rman_backup.strip() == '':
        rman_backup = '无'
    return rman_backup


def deal_session(curs):
    session = ['','','','']
    for i in curs:
        session[0] = i[0]
        session[1] = i[1]
        session[2] = i[2]
        session[3] = i[3]
    return session


def deal_user(curs):
    user_info = {'username':'' , 'status':'', 'expired':''}
    for i in curs:
        user_info['username'] = user_info['username'] + spacing + str(i[0]) + '\n'
        user_info['status'] = user_info['status'] + spacing + str(i[1]) + '\n'
        time = i[2]
        user_info['expired'] = user_info['expired'] + spacing + str(time) + '\n'
    return user_info

## 测试
def main():
    ora_list = [0,'t11gdb','N','192.168.22.211','6666','lanmc','lanmc123','t11gdb']
    db_ip = ora_list[3]
    db_port = ora_list[4]
    db_inst = ora_list[7]
    db_user = ora_list[5]
    passwd = ora_list[6]
    oracle_url = '{}:{}/{}'.format(db_ip, db_port, db_inst)
    conn = cx_Oracle.connect(db_user, passwd, oracle_url)
    curs = conn.cursor()
    curs.execute(sql.sql_users)
    user_info = deal_user(curs)
    print(user_info['username'],user_info['status'],user_info['expired'])

if __name__ == '__main__':
    main()
