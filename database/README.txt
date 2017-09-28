This is a quick guide to get an encrypted database

From your terminal, get sqlcipher

sudo apt-get install sqlcipher

When done, run 
sqlcipher

> .open testing.db
> PRAGMA key='testing';
> create table people (name text primary key);
> insert into people (name) values ('charlie'), ('huey');
> .quit

This should generate a database that will be encrypted unless the correct key is used to access it. If you want to check the contents of the encrypted database run
hexdump -C testing.db

A python library is available to interact with the database. Next step is to generate the needed tables for the database and update the python scripts to use it.



