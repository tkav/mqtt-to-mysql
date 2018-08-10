# mqtt-to-mysql
MQTT topics and data to MySQL database

# About
The insert.py script will subcribe to all MQTT topics ('#') and save the data to a MySQL database.

If a MQTT message is received like this:
```
office {"Humidity":71.40,"Temperature":18.90}
```
Office would be saved as a topic and Humidity and Temperature would be saved as Subtopics.
The values are also split into a 'value' column. The raw_message is also saved.

| idTopic       | idSubTopic    | raw_message                             | value         |
| ------------- | ------------- | -------------                           | ------------- |
| 1             | 1             | {"Humidity":71.40,"Temperature":18.90}  | 71.40         |
| 1             | 2             | {"Humidity":71.40,"Temperature":18.90}  | 18.90         |

# Setup

1. Create Schema - Run DB.sql to create the 'mqtt' database with the table.
2. Change database details - Configure the MySQL host, username and password in the 'insert.py' script.
3. Insert MQTT Data - Run 'insert.py' to start collecting MQTT topics, subtopics and data.
