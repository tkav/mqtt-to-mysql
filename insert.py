#!/usr/bin/python
import MySQLdb
import paho.mqtt.subscribe as subscribe
import json
import datetime

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="username",         # your username
                     passwd="password",  # your password
                     db="mqtt")        # name of the database

def on_message(client, userdata, message):

    print("%s %s" % (message.topic, message.payload))
    topic = message.topic
    value = message.payload
    print("topic is %s" % (topic))
    print("value is %s" % (value))
    topicstring = str(topic)

    cur = db.cursor()
    cur.execute("SELECT * FROM topics WHERE topic = '%s'" % (topic))

    numrows = cur.rowcount

    if numrows == 0:
        print ('%s does not exist in db. Adding..' % (topic))

        now = datetime.datetime.now()
        formatteddate = now.strftime('%Y-%m-%d %H:%M:%S')
        formatteddate = str(formatteddate)

        sql = ("INSERT INTO topics (`topic`, `lastMessage`) VALUES ('%s', '%s')" % (topicstring, formatteddate))
        print sql
        cur.execute(sql)
        db.commit()

    else:
        for row in cur.fetchall():
            idTopics = row[0]
            topicdesc = row[1]

            print topicdesc
            if "{" not in value:

                now = datetime.datetime.now()
                formatteddate = now.strftime('%Y-%m-%d %H:%M:%S')
                formatteddate = str(formatteddate)

                sql = "INSERT INTO `values` (`idTopic`, `raw_message`, `value`, `received`) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (idTopics, value, value, formatteddate))
                db.commit()

            else:
                print "contains '{'"

                #split json
                data = json.loads(value)
                for key, val in data.items():
                    #check if subtopic exists
                    print key, val
                    cur.execute("SELECT * FROM sub_topics WHERE idTopic = %s AND subtopic = '%s'" % (idTopics, key))
                    numrows = cur.rowcount

                    if numrows == 0:
                        print ('%s subtopic does not exist in db. Adding..' % (key))

                        sql = "INSERT INTO `sub_topics` (`idTopic`, `subtopic`) VALUES (%s, %s)"
                        cur.execute(sql, (idTopics, key))
                        db.commit()

                    else:
                        #subtopic exists

                        #Add data (val) against subtopic id
                        for row in cur.fetchall():
                            idSubTopics = row[0]

                            now = datetime.datetime.now()
                            formatteddate = now.strftime('%Y-%m-%d %H:%M:%S')
                            formatteddate = str(formatteddate)

                            sql = "INSERT INTO `values` (`idTopic`, `idSubTopic`, `raw_message`, `value`, `received`) VALUES (%s, %s, %s, %s, %s)"
                            cur.execute(sql, (idTopics, idSubTopics, value, val, formatteddate))
                            db.commit()

    cur.close()

subscribe.callback(on_message, "#", hostname="192.168.1.112")
