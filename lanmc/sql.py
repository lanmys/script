## 存放sql脚本




def sql_dbname(ispdb):
    if ispdb == 'Y' or ispdb =='y':
        sql = 'select PDB_NAME from cdb_pdbs'
        return sql
    else:
        sql = 'select name from v$database'
        return sql


sql_open_mode ='select OPEN_MODE from v$database'


sql_tablespace = '''SELECT UPPER(T.TABLESPACE_NAME) TABLESPACE_NAME,
          TO_CHAR(ROUND((D.BYTES_MB-NVL(F.FREE_BYTES_MB,0))/T.TOTAL_BYTES_MB*100,2),\'990.99\') "USED_RATE_%",
          (T.TOTAL_BYTES_MB-(D.BYTES_MB-NVL(F.FREE_BYTES_MB,0))) FREE_BYTES_MB
   FROM ( SELECT TABLESPACE_NAME,ROUND(SUM(BYTES)/1024/1024) FREE_BYTES_MB,ROUND(MAX(BYTES)/(1024*1024),2) MAX_FREE_BYTES_MB
         FROM SYS.DBA_FREE_SPACE  GROUP BY TABLESPACE_NAME ) F,
        ( select tablespace_name, ROUND(sum(decode(AUTOEXTENSIBLE,\'YES\',MAXBYTES,\'NO\',BYTES))/1024/1024) TOTAL_BYTES_MB
          FROM SYS.DBA_DATA_FILES   GROUP BY TABLESPACE_NAME ) T,( SELECT TABLESPACE_NAME,ROUND(SUM(BYTES)/1024/1024) BYTES_MB
         FROM SYS.DBA_DATA_FILES GROUP BY TABLESPACE_NAME ) D
   WHERE T.TABLESPACE_NAME=F.TABLESPACE_NAME(+)
   AND   T.TABLESPACE_NAME=D.TABLESPACE_NAME
   AND 	ROUND((D.BYTES_MB-NVL(F.FREE_BYTES_MB,0))/T.TOTAL_BYTES_MB*100,2) > 85'''


sql_asm = '''select a.name,decode(a.type,\'NORMAL\',a.total_mb/2,a.total_mb) as total_mb,  
round(100*((decode(a.type,\'NORMAL\',a.total_mb/2-a.usable_file_mb,a.total_mb-a.usable_file_mb))/decode(a.type,\'NORMAL\',a.total_mb/2,a.total_mb)),2)  as usage_rate, 
a.usable_file_mb/1024 as usable_file_G from v$asm_diskgroup a,v$database b where total_mb>0
and round(100*((decode(a.type,\'NORMAL\',a.total_mb/2-a.usable_file_mb,a.total_mb-a.usable_file_mb))/decode(a.type,\'NORMAL\',a.total_mb/2,a.total_mb)),2)>85'''

sql_datafile = '''select FILE_NAME,TABLESPACE_NAME,ONLINE_STATUS from dba_data_files 
                    where ONLINE_STATUS not in (\'ONLINE\',\'SYSTEM\')'''

sql_dbtime = '''select /*+MATERIALIZE*/ e.instance_number inst_id,e.snap_id snap_id,BEGIN_INTERVAL_TIME
      ,round((lead(e.value) over(partition by e.instance_number order by e.snap_id) - e.value)/1000000,0) DBTIME
      ,round( (lead(e.value) over(partition by e.instance_number order by e.snap_id) - e.value)/1000000/((to_number(to_date(to_char(END_INTERVAL_TIME,\'yyyymmddhh24miss\'),\'yyyymmddhh24miss\')-to_date(to_char(BEGIN_INTERVAL_TIME,\'yyyymmddhh24miss\'),\'yyyymmddhh24miss\')))*86400),1) DBTIME_PERSEC
      from dba_hist_sys_time_model e, DBA_HIST_SNAPSHOT s
      where s.snap_id = e.snap_id
       and e.instance_number = s.instance_number
       and stat_name= \'DB time\' 
       and s.begin_interval_time >= sysdate-1'''


sql_rman = '''select input_type,STATUS,start_time,end_time,INPUT_BYTES_DISPLAY,OUTPUT_BYTES_DISPLAY,TIME_TAKEN_DISPLAY 
                from v$rman_backup_job_details
                where start_time > sysdate - 2
                order by start_time'''

sql_session = '''select RESOURCE_NAME,CURRENT_UTILIZATION,MAX_UTILIZATION,LIMIT_VALUE from gv$resource_limit 
                where resource_name= \'sessions\' order by resource_name, inst_id'''


sql_users = '''select USERNAME,ACCOUNT_STATUS,EXPIRY_DATE from dba_users where ACCOUNT_STATUS <> 'OPEN' AND username not in (\'SYS\',
\'SYSTEM\',\'XS$NULL\',\'OJVMSYS\',\'LBACSYS\',\'OUTLN\',\'SYS$UMF\',\'DBSNMP\',\'APPQOSSYS\',\'DBSFWUSER\',\'GGSYS\',
\'ANONYMOUS\',\'CTXSYS\',\'DVSYS\',\'DVF\',\'GSMADMIN_INTERNAL\',\'MDSYS\',\'OLAPSYS\',\'XDB\',\'WMSYS\',\'GSMCATUSER\',
\'MDDATA\',\'SYSBACKUP\','REMOTE_SCHEDULER_AGENT','GSMUSER','SYSRAC','GSMROOTUSER','SI_INFORMTN_SCHEMA',
\'AUDSYS\',\'DIP\',\'ORDPLUGINS\',\'SYSKM\',\'ORDDATA\',\'ORACLE_OCM\',\'SYSDG\',\'ORDSYS\',\'SPATIAL_CSW_ADMIN_USR\',
\'SPATIAL_WFS_ADMIN_USR\',\'FLOWS_FILES\',\'APEX_030200\',\'OWBSYS_AUDIT\',\'EXFSYS\',\'OWBSYS\',\'APEX_PUBLIC_USER\',\'SCOTT\')'''

'''



'''