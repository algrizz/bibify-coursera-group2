# -*- coding: utf-8 -*-
#
# This python file removes the existing database and creates a new clean one
# 
#

from pysqlcipher3 import dbapi2 as sqlcipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

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
    db_key = get_random_bytes(32)
    # Cipher the keys and store them in the key_storage.db
    cursor = db.cursor()
    cyphered_key, tag = cipher.encrypt_and_digest(db_key);
    cursor.execute("insert into app_keys (name, nonce, tag, key_val) values (?, ?, ?, ?);",
                [el, cipher.nonce, tag, cyphered_key])
    cipher = AES.new(db_master_key.encode('utf-8'), AES.MODE_EAX)

# Disconnect from the db
db.commit()
db.close()

















































#db.close()