# README #

### What is this repository for? ###

* python3 code for taking MSSQL RDS backups using the AWS stored procedure which generates a backup and stores it in S3 
* There is a limitation with RDS snapshots as it will take a backup of the entire server. If you wish to restore a database on a server with many databases, using AWS snapshots can prove to be difficult/annoying.
* AWS has provided a stored procedure to store a backup of an individual database to S3
* The python code has troubles running in AWS Lambda, This version will only work via an Ubuntu based system.
* Version 1 

### How do I get set up? ###

#### Summary of set up ####
* Python script will utilize the following modules
      * pymssql - Used for connecting to MS SQL DB
      * Json, sys - Only used for manual execution via cli not AWS Lambda
      * time - Used to query current time
      * credstash - Used to query secrets stored in Dynamodb encrypted using KMS
#### Configuration ####
* Installed the modules above
* create a test with the following json. You can replace the foo and bar with your own database names
```json
{
  "databasename: [
    "foo",
    "bar"
  ]
}
```
#### Dependencies ####
* N/A
* How to run tests
  * Ensure the following environment variables are exported
  	* RDS_HOSTNAME = the hostname of the RDS
	* CREDSTASH_USERNAME_PATH = The path to the username in credstash. i.e `credstash get $CREDSTASH_USERNAME_PATH`
	* CREDSTASH_PASSWORD_PATH = The path to the password in credstash i.e `credstash  get CREDSTASH_PASSWORD_PATH`
	* AWS_RDS_KMS_KEY_ARN = ARN to the KMS key to ensure your backups are encrypted
	* AWS_S3_BUCKET_ARN = ARN to the S3 Bucket where you wish to store your backup
  * Tests can be performed via linux CLI. Ensure the modules explained above are installed. To run a test perform the following. `cat example_event.json| python3 backup.py`
* Deployment instructions
  * Ensure tests are performed to the develop branch first, or checkout master in your own branch. Once tested, merge to master. Please ensure to create tags with each release to master.

### Who do I talk to? ###

* Repo owner or admin
* Nikola Sepentulevski
