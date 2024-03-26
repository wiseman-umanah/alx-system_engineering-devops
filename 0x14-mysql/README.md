## MYSQL MASTER_REPLICA 

MySQL replication offers a dependable method for data distribution, load balancing, and protecting against data loss by using a master-slave architecture, where the master database acts as the source of truth and the slave databases duplicate changes from the master.

## UNDERSTANDING REPLICATION IN MYSQL

In MySQL, replication involves the source database writing down every change made to the data held within one or more databases in a special file known as the binary log. Once the replica instance has been initialized, it creates two threaded processes. The first, called the IO thread, connects to the source MySQL instance and reads the binary log events line by line, and then copies them over to a local file on the replica’s server called the relay log. The second thread, called the SQL thread, reads events from the relay log and then applies them to the replica instance as fast as possible.

## THE SETUP

# Step 1 — Adjusting Your Source Server’s Firewall
Assuming you followed the prerequisite Initial Server Setup Guide, you will have configured a firewall on both your servers with UFW. This will help to keep both your servers secure, but the source’s firewall will block any connection attempts from your replica MySQL instance.

To change this, you’ll need to include a UFW rule that allows connections from your replica through the source’s firewall. You can do this by running a command like the following on your source server.

This particular command allows any connections that originate from the replica server’s IP address — represented by replica_server_ip — to MySQL’s default port number, 3306:

`sudo ufw allow from replica_server_ip to any port 3306` -- source
Be sure to replace replica_server_ip with your replica server’s actual IP address. If the rule was added successfully you’ll see the following output:


# Step 2 — Configuring the Source Database
In order for your source MySQL database to begin replicating data, you need to make a few changes to its configuration.

On Ubuntu 20.04, the default MySQL server configuration file is named mysqld.cnf and can be found in the /etc/mysql/mysql.conf.d/ directory. Open this file on the source server with your preferred text editor. Here, we’ll use nano:

`sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf`
Within the file, find the bind-address directive. It will look like this by default:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
bind-address            = 127.0.0.1
. . .
```
Replace 127.0.0.1 with the source server’s IP address. After doing so, the bind-address directive will look like this, with your own server’s IP address in place of source_server_ip:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
bind-address            = source_server_ip
. . .
```

Next, find the server-id directive, which defines an identifier that MySQL uses internally to distinguish servers in a replication setup. Every server in a replication environment, including the source and all its replicas, must have their own unique server-id value. This directive will be commented out by default and will look like this:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
# server-id             = 1
. . .
```
Uncomment this line by removing the pound sign (#). You can choose any number as this directive’s value, but remember that the number must be unique and cannot match any other server-id in your replication group. To keep things simple the following example leaves this value as the default, 1:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
server-id               = 1
. . .
```
Below the server-id line, find the log_bin directive. This defines the base name and location of MySQL’s binary log file.

When commented out, as this directive is by default, binary logging is disabled. Your replica server must read the source’s binary log file so it knows when and how to replicate the source’s data, so uncomment this line to enable binary logging on the source. After doing so, it will look like this:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
log_bin                       = /var/log/mysql/mysql-bin.log
. . .
```
Lastly, scroll down to the bottom of the file to find the commented-out binlog_do_db directive:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
# binlog_do_db          = include_database_name
```
Remove the pound sign to uncomment this line and replace include_database_name with the name of the database you want to replicate. This example shows the binlog_do_db directive pointing to a database named db, but if you have an existing database on your source that you want to replicate, use its name in place of db:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
binlog_do_db          = db
```
Note: If you want to replicate more than one database, you can add another binlog_do_db directive for every database you want to add. This tutorial will continue on with replicating only a single database, but if you wanted to replicate more it might look like this:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
binlog_do_db          = db
binlog_do_db          = db_1
binlog_do_db          = db_2
```
Alternatively, you can specify which databases MySQL should not replicate by adding a binlog_ignore_db directive for each one:
```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
binlog_ignore_db          = db_to_ignore
```
After making these changes, save and close the file. If you used nano to edit the file, do so by pressing CTRL + X, Y, and then ENTER.

Then restart the MySQL service by running the following command:

`sudo systemctl restart mysql`
With that, this MySQL instance is ready to function as the source database which your other MySQL server will replicate. Before you can configure your replica, though, there are still a few more steps you need to perform on the source to ensure that your replication topology will function correctly. The first of these is to create a dedicated MySQL user which will perform any actions related to the replication process.

# Step 3 — Creating a Replication User
Each replica in a MySQL replication environment connects to the source database with a username and password. Replicas can connect using any MySQL user profile that exists on the source database and has the appropriate privileges, but this tutorial will outline how to create a dedicated user for this purpose.

Start by opening up the MySQL shell:

`sudo mysql` -- source
Note: If you configured a dedicated MySQL user that authenticates using a password, you can connect to your MySQL with a command like this instead:

`mysql -u sammy -p ` -- source
Replace sammy with the name of your dedicated user, and enter this user’s password when prompted.

Be aware that some operations throughout this guide, including a few that must be performed on the replica server, require advanced privileges. Because of this, it may be more convenient to connect as an administrative user, as you can with the previous sudo mysql command. If you want to use a less privileged MySQL user throughout this guide, though, they should at least be granted the CREATE USER, RELOAD, REPLICATION CLIENT, REPLICATION SLAVE, and REPLICATION_SLAVE_ADMIN privileges.

From the prompt, create a new MySQL user. The following example will create a user named replica_user, but you can name yours whatever you’d like. Be sure to change replica_server_ip to your replica server’s public IP address and to change password to a strong password of your choosing:

`CREATE USER 'replica_user'@'replica_server_ip' IDENTIFIED WITH mysql_native_password BY 'password';` -- source
Note that this command specifies that replica_user will use the mysql_native_password authentication plugin. It’s possible to instead use MySQL’s default authentication mechanism, caching_sha2_password, but this would require setting up an encrypted connection between the source and the replica. This kind of setup would be optimal for production environments, but configuring encrypted connections is beyond the scope of this tutorial. The MySQL documentation includes instructions on how to configure a replication environment that uses encrypted connections if you’d like to set this up.

After creating the new user, grant them the appropriate privileges. At minimum, a MySQL replication user must have the REPLICATION SLAVE permissions:

`GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'replica_server_ip';`
Following this, it’s good practice to run the FLUSH PRIVILEGES command. This will free up any memory that the server cached as a result of the preceding CREATE USER and GRANT statements:

`FLUSH PRIVILEGES;`
With that, you’ve finished setting up a replication user on your source MySQL instance. However, do not exit the MySQL shell. Keep it open for now, as you’ll use it in the next step to obtain some important information about the source database’s binary log file.

# Step 4 — Retrieving Binary Log Coordinates from the Source
Recall from the Understanding Replication in MySQL section that MySQL implements replication by copying database events from the source’s binary log file line by line and implementing each event on the replica. When using MySQL’s binary log file position-based replication, you must provide the replica with a set of coordinates that detail the name of the source’s binary log file and a specific position within that file. The replica then uses these coordinates to determine the point in the log file from which it should begin copying database events and track which events it has already processed.

This step outlines how to obtain the source instance’s current binary log coordinates in order to set your replicas to begin replicating data from the latest point in the log file. To make sure that no users change any data while you retrieve the coordinates, which could lead to problems, you’ll need to lock the database to prevent any clients from reading or writing data as you obtain the coordinates. You will unlock everything shortly, but this procedure will cause your database to go through some amount of downtime.

You should still have your source server’s MySQL shell open from the end of the previous step. From the prompt, run the following command which will close all the open tables in every database on your source instance and lock them:

`FLUSH TABLES WITH READ LOCK;`
Then run the following operation which will return the current status information for the source’s binary log files:

`SHOW MASTER STATUS;`
You will see a table similar to this example in your output:
```
Output
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      899 | db           |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```
This is the position from which the replica will start copying database events. Record the File name and the Position value, as you will need these later when you initiate replication.

What you do immediately after obtaining this information depends on whether your source database has any existing data you want to migrate over to your replicas. Jump to whichever of the two following subsections makes the most sense for your situation.

If Your Source Doesn’t Have Any Existing Data to Migrate
If your source MySQL instance is a new installation or doesn’t have any existing data you want to migrate to your replicas, you can at this point unlock the tables:

`UNLOCK TABLES;`
If you haven’t done so already, you could create the database you’ve chosen to replicate while you still have the MySQL shell open. In keeping with the example given in Step 2, the following operation will create a database named db:

`CREATE DATABASE db;`

After that, close the MySQL shell:

`exit`
Following that, you can move on to the next step.

If Your Source Has Existing Data to Migrate
If you have data on your source MySQL instance that you want to migrate to your replicas, you can do so by creating a snapshot of the database with the mysqldump utility. However, your database should still be currently locked. If you make any new changes in the same window, the database will automatically unlock. Likewise, the tables will automatically unlock if you exit the client.

Unlocking the tables could lead to problems since it would mean that clients could again change the data in the database. This could potentially lead to a mismatch between your data snapshot and the binary log coordinates you just retrieved.

For this reason, you must open a new terminal window or tab on your local machine so you can create the database snapshot without unlocking MySQL.

From the new terminal window or tab, open up another SSH session to the server hosting your source MySQL instance:

`ssh sammy@source_server_ip`
Then, from the new tab or window, export your database using mysqldump. The following example creates a dump file named db.sql from a database named db, but make sure you include the name of your own database instead. Also, be sure to run this command in the bash shell, not the MySQL shell:

`sudo mysqldump -u root db > db.sql`
Following that you can close this terminal window or tab and return to your first one, which should still have the MySQL shell open. From the MySQL prompt, unlock the databases to make them writable again:

`UNLOCK TABLES;`
Then you can exit the MySQL shell:

`exit`
You can now send your snapshot file to your replica server. Assuming you’ve configured SSH keys on your source server and have added the source’s public key to your replica’s authorized_keys file, you can do this securely with an scp command like this:

`scp db.sql sammy@replica_server_ip:/tmp/`
Be sure to replace sammy with the name of the administrative Ubuntu user profile you created on your replica server, and to replace replica_server_ip with the replica server’s IP address. Also, note that this command places the snapshot in the replica server’s /tmp/ directory.

After sending the snapshot to the replica server, SSH into it:

`ssh sammy@replica_server_ip`
Then open up the MySQL shell:

`sudo mysql` -- replica
From the prompt, create the new database that you will be replicating from the source:

`CREATE DATABASE db;` -- replica
You don’t need to create any tables or load this database with any sample data. That will all be taken care of when you import the database using the snapshot you just created. Instead, exit the MySQL shell:

`exit`
Then import the database snapshot:

`sudo mysql db < /tmp/db.sql`
Your replica now has all the existing data from the source database. You can complete the final step of this guide to configure your replica server to begin replicating new changes made on the source database.

# Step 5 — Configuring the Replica Database
All that’s left to do is to change the replica’s configuration similar to how you changed the source’s. Open up the MySQL configuration file, mysqld.cnf, this time on your replica server:

`sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf`
As mentioned previously, each MySQL instance in a replication setup must have a unique server-id value. Find the replica’s server-id directive, uncomment it, and change its value to any positive integer, as long as it’s different from that of the source:

```
/etc/mysql/mysql.conf.d/mysqld.cnf
server-id               = 2
``` -- replica

Following that, update the log_bin and binlog_do_db values so that they align with the values you set in the source machine’s configuration file:

```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
log_bin                 = /var/log/mysql/mysql-bin.log
. . .
binlog_do_db            = db
. . .
``` -- replica

Lastly, add a relay-log directive defining the location of the replica’s relay log file. Include the following line at the end of the configuration file:

```
/etc/mysql/mysql.conf.d/mysqld.cnf
. . .
relay-log               = /var/log/mysql/mysql-relay-bin.log
``` -- replica

After making these changes, save and close the file. Then restart MySQL on the replica to implement the new configuration:

`sudo systemctl restart mysql` -- replica
After restarting the mysql service, you’re finally ready to start replicating data from your source database.

# Step 6 — Starting and Testing Replication
At this point, both of your MySQL instances are fully configured to allow replication. To start replicating data from your source, open up the the MySQL shell on your replica server:

`sudo mysql` -- replica
From the prompt, run the following operation, which configures several MySQL replication settings at the same time. After running this command, once you enable replication on this instance it will try to connect to the IP address following SOURCE_HOST using the username and password following SOURCE_USER and SOURCE_PASSWORD, respectively. It will also look for a binary log file with the name following SOURCE_LOG_FILE and begin reading it from the position after SOURCE_LOG_POS.

Be sure to replace source_server_ip with your source server’s IP address. Likewise, replica_user and password should align with the replication user you created in Step 2; and mysql-bin.000001 and 899 should reflect the binary log coordinates you obtained in Step 3.

You may want to type this command out in a text editor before running it on your replica server so that you can more easily replace all the relevant information:
```
CHANGE REPLICATION SOURCE TO
SOURCE_HOST='source_server_ip',
SOURCE_USER='replica_user',
SOURCE_PASSWORD='password',
SOURCE_LOG_FILE='mysql-bin.000001',
SOURCE_LOG_POS=899;
``` -- replica
Following that, activate the replica server:

`START REPLICA;` -- replica
If you entered all the details correctly, this instance will begin replicating any changes made to the db database on the source.

You can see details about the replica’s current state by running the following operation. The \G modifier in this command rearranges the text to make it more readable:

`SHOW REPLICA STATUS\G;` -- replica
This command returns a lot of information which can be helpful when troubleshooting:
```
Output
*************************** 1. row ***************************
             Replica_IO_State: Waiting for master to send event
                  Source_Host: 138.197.3.190
                  Source_User: replica_user
                  Source_Port: 3306
                Connect_Retry: 60
              Source_Log_File: mysql-bin.000001
          Read_Source_Log_Pos: 1273
               Relay_Log_File: mysql-relay-bin.000003
                Relay_Log_Pos: 729
        Relay_Source_Log_File: mysql-bin.000001
. . .
``` -- replica
Note: If your replica has an issue in connecting or replication stops unexpectedly, it may be that an event in the source’s binary log file is preventing replication. In such cases, you could run the SET GLOBAL SQL_SLAVE_SKIP_COUNTER command to skip a certain number of events following the binary log file position you defined in the previous command. This example only skips the first event:

`SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;` -- replica
Following that, you’d need to start the replica again:

`START REPLICA;` -- replica
Also, if you ever need to stop replication, note that you can do so by running the following operation on the replica instance:

`STOP REPLICA;` -- replica
Your replica is now replicating data from the source. Any changes you make to the source database will be reflected on the replica MySQL instance. You can test this by creating a sample table on your source database and checking whether it gets replicated successfully.

Begin by opening up the MySQL shell on your source machine:

`sudo mysql`
Select the database you chose to replicate:

`USE db;`
Then create a table within that database. The following SQL operation creates a table named example_table with one column named example_column:
```
CREATE TABLE example_table (
example_column varchar(30)
);
Output
Query OK, 0 rows affected (0.03 sec)
If you’d like, you can also add some sample data to this table:

INSERT INTO example_table VALUES
('This is the first row'),
('This is the second row'),
('This is the third row');
Output
Query OK, 3 rows affected (0.03 sec)
Records: 3  Duplicates: 0  Warnings: 0
```
After creating a table and optionally adding some sample data to it, go back to your replica server’s MySQL shell and select the replicated database:

``USE db;`` -- replica
Then run the SHOW TABLES statement to list all the tables within the selected database:

``SHOW TABLES;`` -- replica
If replication is working correctly, you’ll see the table you just added to the source listed in this command’s output:
```
Output
+---------------+
| Tables_in_db  |
+---------------+
| example_table |
+---------------+
1 row in set (0.00 sec)
``` -- replica
Also, if you added some sample data to the table on the source, you can check whether that data was also replicated with a query like the following:

`SELECT * FROM example_table;` -- replica
In SQL, an asterisk (*) is shorthand “all columns.” So this query essentially tells MySQL to return every column from example_table. If replication is working as expected, this operation will return that data in its output:

```Output
+------------------------+
| example_column         |
+------------------------+
| This is the first row  |
| This is the second row |
| This is the third row  |
+------------------------+
3 rows in set (0.00 sec)
```-- replica
If either of these operations fail to return the example table or data that you added to the source, it may be that you have an error somewhere in your replication configuration. In such cases, you could run the SHOW REPLICA STATUS\G operation to try finding the cause of the issue. Additionally, you can consult MySQL’s documentation on troubleshooting replication for suggestions on how to resolve replication problems.
