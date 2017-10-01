# -*- coding: utf-8 -*-
#
# This python file removes the existing database and creates a new clean one
# 
#

from pysqlcipher3 import dbapi2 as sqlcipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import binascii

###############################################################################
#
# Remove existing databases and create new key storage 
#
###############################################################################

db_keys = "key_storage.db"
db_messages = "messages.db"
db_users = "users.db"
db_sessions = "sessions.db"

db_array = [db_keys, db_messages, db_users, db_sessions]

# Delete existing databases and create them anew to start from a clean state
for el in db_array:
    path_to_db = "./" + el
    os.system('rm -f ' + path_to_db)
    os.system('echo ".open ' + path_to_db + ' .quit" | sqlcipher')

path_to_master_key = "./.key/master_db_key"
fp = open(path_to_master_key, "r")
db_master_key = fp.readlines()[0][:-1]

# Create the database to store the keys to the other databases
db = sqlcipher.connect(db_keys)
db.executescript('pragma key="' + db_master_key + '"; pragma kdf_iter=64000;')
db.executescript('create table app_keys ' 
                + '(name text primary key,' 
                + ' nonce binary[32],' 
                + ' tag binary[32],'
                + ' key_val binary[32]);')

# Initialize the cipher
cipher = AES.new(db_master_key.encode('utf-8'), AES.MODE_EAX)

# Generate and store the keys for the other databases
for el in db_array[1:]:
    # Generate a random key for the database
    db_key = binascii.hexlify(get_random_bytes(16))
    # Cipher the keys and store them in the key_storage.db
    cursor = db.cursor()
    cyphered_key, tag = cipher.encrypt_and_digest(db_key);
    cursor.execute("insert into app_keys (name, nonce, tag, key_val)"
                    + " values (?, ?, ?, ?);",
                    [el, cipher.nonce, tag, cyphered_key])
    cipher = AES.new(db_master_key.encode('utf-8'), AES.MODE_EAX)

# Store persistently the recently added entries
db.commit()

###############################################################################
#
# Initialize users table that will be used to store users information
#
###############################################################################

# Retrieve key from key_storage database
name, nonce, tag, ciphertext = db.execute('select * from app_keys where '
                    + 'name="' + db_users + '";').fetchone()
cipher = AES.new(db_master_key.encode('utf-8'), AES.MODE_EAX, nonce)
user_db_key = cipher.decrypt_and_verify(ciphertext, tag)

# Open users database and create associated tables
user_db = sqlcipher.connect(db_users)

print("users key: " + user_db_key.decode('utf-8')) # -- for debbuggin purposes only
user_db.executescript("pragma key='" + user_db_key.decode('utf-8') + "'; pragma kdf_iter=64000;")
user_db.executescript('create table unverified_user ' 
                        + '(id integer primary key,' 
                        + ' email varchar(60) not null,' 
                        + ' code char(41) not null);')
                        
user_db.executescript('create table users ' 
                        + '(id integer primary key,' 
                        + ' fullname varchar(60) not null,' 
                        + ' pass varchar(100) not null,' 
                        + ' email varchar(60) unique not null,' 
                        + ' verified tinyint(1) default null);')

user_db.executescript('create table secondfactor ' 
                        + '(id integer primary key,' 
                        + ' email varchar(60) not null,' 
                        + ' code char(41) not null);')                        

# We haven't introduced any user, so no need to commit, just close
user_db.close()

###############################################################################
#
# Initialize messages table that will be used to store messages
#
###############################################################################

# Retrieve key from key_storage database
name, nonce, tag, ciphertext = db.execute('select * from app_keys where '
                    + 'name="' + db_messages + '";').fetchone()
cipher = AES.new(db_master_key.encode('utf-8'), AES.MODE_EAX, nonce)
message_db_key = cipher.decrypt_and_verify(ciphertext, tag)

# Open messages database and create associated tables
message_db = sqlcipher.connect(db_messages)

print("messages key: " + message_db_key.decode('utf-8')) # -- for debbuggin purposes only
message_db.executescript("pragma key='" + message_db_key.decode('utf-8') + "'; pragma kdf_iter=64000;")
message_db.executescript('create table messageboard ' 
                        + '(id integer primary key,' 
                        + ' msg varchar(500) not null,' 
                        + ' title varchar(50) not null,' 
                        + ' source varchar(60) not null,' 
                        + ' destination varchar(60) not null);')

# We haven't introduced any message, so no need to commit, just close
message_db.close()

# Disconnect from the db
db.close()
