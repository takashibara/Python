import datetime
from datetime import timedelta
import locale

#今の日付を取得
now = datetime.datetime.now();
print(now);

#3日後
aft_3days = now + timedelta(days=3);
print(aft_3days);

#3日後
aft_3days = now + timedelta(days=3);
print(aft_3days);

#フォーマット変換
dateStr = "{0:%Y%m%d}".format(now);
print(dateStr);

#フォーマット変換
dateStr2 = "{0:%Y/%m/%d(%A)%H:%M:%S}".format(now);
print(dateStr2);

#この書き方が手っ取り早そう
str_now = now.strftime('%Y/%m/%d');
print(str_now);

#日付チェックの関数
def checkDate():
    now = datetime.datetime.now();