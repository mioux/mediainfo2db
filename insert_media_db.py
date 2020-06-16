#!/usr/bin/env python
# -*- coding: utf-8 -*
from config import *

import MySQLdb
import sys
import os.path
import subprocess
import json

if len(sys.argv) == 1:
    sys.stderr.write("File is missing\n")
    sys.exit(1)

if len(sys.argv) > 2:
    sys.stderr.write("Too much arguments\n")
    sys.exit(1)

if os.path.isfile(sys.argv[1]) == False:
    sys.stderr.write("File does not exists\n")
    sys.exit(1)

paramMysql = {
    'host'       : MYSQL_HOST,
    'port'       : MYSQL_PORT,
    'user'       : MYSQL_USER,
    'passwd'     : MYSQL_PASSWORD,
    'db'         : MYSQL_DB
}

proc = subprocess.run(
    ['mediainfo', '--Output=JSON', sys.argv[1] ],
    stdout=subprocess.PIPE
)
media_info = proc.stdout.decode("utf-8")[:-1]

proc = subprocess.run(
    ['realpath', sys.argv[1] ],
    stdout=subprocess.PIPE
)
realpath = proc.stdout.decode("utf-8")[:-1]

sql = "SELECT media_id FROM media_file WHERE media_filename = %(realpath)s"

conn = MySQLdb.connect(**paramMysql)
conn.paramstyle = 'pyformat'
conn.autocommit(True)
cur = conn.cursor(MySQLdb.cursors.DictCursor)
cur.execute(sql, { 'realpath': realpath })
rows = cur.fetchall()

if cur.rowcount == 0:
    sql = "INSERT INTO media_file (media_filename) VALUES (%(realpath)s);"
    cur.execute(sql, { 'realpath': realpath })
    media_id = cur.lastrowid
else:
    for row in rows:
        media_id = row['media_id']

media_json = json.loads(media_info)['media']

for track in media_json["track"]:
    sql = "SELECT track_type_id FROM ref_media_track_type WHERE track_type_label = %(type)s"
    cur.execute(sql, { 'type': track["@type"] })
    rows = cur.fetchall()
    for row in rows:
        track_type_id = row["track_type_id"]
        StreamOrder = int(track.get("StreamOrder", -1))
        if StreamOrder == -1:
            StreamOrder = track.get("@typeorder", 0)


        sql = """
                REPLACE INTO media_track (
                    track_type_id,
                    media_id,
                    media_index,
                    media_key,
                    media_value
                ) VALUES (
                    %(track_type_id)s,
                    %(media_id)s,
                    %(media_index)s,
                    %(media_key)s,
                    %(media_value)s
                )
              """
        for key in track:
            if key != "@type":
                cur.execute(sql, { 
                    'track_type_id': int(track_type_id),
                    'media_id': int(media_id),
                    'media_index': int(StreamOrder),
                    'media_key': str(key),
                    'media_value': str(track[key])
                })

print ("Media updated : " + realpath)    

conn.close()
