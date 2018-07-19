import pymssql
import sys,json
import time
import datetime
import credstash
import os

def lambda_handler(context,event):

    #### Connection Detials
    rds_host=(os.environ['RDS_HOSTNAME'])
    credstash_username=(os.environ['CREDSTASH_USERNAME_PATH'])
    credstash_pass=(os.environ['CREDSTASH_PASSWORD_PATH'])
    rds_username=credstash.getSecret(credstash_username)
    rds_password=credstash.getSecret(credstash_pass)
    rds_database_to_backup = []
    rds_database_to_backup = context['databasename']
    kms_key_arm=(os.environ['AWS_RDS_KMS_KEY_ARN'])
    s3_bucket_arn=(os.environ['AWS_S3_BUCKET_ARN'])
    # now=str(time.strftime("%Y-%m-%d_%H-%M"))
    now='{0:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
    print(now)
    # Connected to DB
    try:
        conn = pymssql.connect(
        server=rds_host,
        user=rds_username,
        password=rds_password
        )
    except Exception as e:
        print(e)
        exit()
    else:
        print("Connected to %s" % (rds_host))

    print("Backing up: %s" % (rds_database_to_backup))

    query_response = []
    for db in rds_database_to_backup:
        query=("exec msdb.dbo.rds_backup_database\n"
            "@source_db_name='%s',\n"
            "@s3_arn_to_backup_to='%s',\n"
            "@kms_master_key_arn='%s',\n"
            "@overwrite_S3_backup_file=1,\n"
            "@type='FULL';" % (db,(s3_bucket_arn+db+"-"+now+".bak"),kms_key_arm))
        # query='SELECT * from EvolutionCommon.dbo._btblRegCode3'
        # print(query)
        try:
            print('trying query')
            cursor=conn.cursor()
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
            print("QUERY FAILED!!!")
            # Close connection
            conn.close()
        else:
            exit()


    # Return the Task in json
    for response in query_response:
        # print(response[0])
        for task in response:
            task_id=task[0]
            task_type=task[1]
            databse_name=task[5]
            s3_object_arn=task[6]
            print(json.dumps(
            {
            "task_id": task_id,
            "task_type": task_type,
            "database_name": databse_name,
            "s3_object_arn": s3_object_arn
            }
            ))
    # Close connection
    conn.close()

if __name__ == '__main__':
    context = json.load( sys.stdin )
    event=""
    lambda_handler(context,event)
