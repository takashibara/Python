import MySQLdb

# MySQLの接続情報（各自の環境にあわせて設定のこと）
db_config = {
    'host': 'localhost',
    'db': 'mydata',  # Database Name
    'user': 'root',
    'passwd': '',
    'charset': 'utf8',
}

try:
    # 接続
    conn = MySQLdb.connect(host=db_config['host'], db=db_config['db'], user=db_config['user'],
                           passwd=db_config['passwd'], charset=db_config['charset'])

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM test')

    # 件数の取得は Cusor オブジェクトの rowcount プロパティー
    print(cursor.rowcount)  # 6

    # 全件取得は cursor.fetchall()
    print(cursor.fetchall())

    for row in cursor:
        print(row[0] + ":" + row[1])

except MySQLdb.Error as ex:
    print('MySQL Error: ', ex)
