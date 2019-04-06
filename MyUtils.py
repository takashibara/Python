##################################################
# ライブラリをインポート
##################################################
import win32com.client;
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from os.path import basename
import datetime
from datetime import timedelta
import shutil
import copy

##################################################
# 非稼働日情報をインポート
##################################################
import NonExeDate

##################################################
# 日付文字列(YYYYMMDD)
##################################################
def getDateStrTodayYYYYMMDD():
	return datetime.datetime.now().strftime('%Y%m%d');

##################################################
# シートに値をセットしてマクロ呼出し
#   args1 フォルダパス 「\\」と記載
#   args2 マクロファイル名
#   args3 実行マクロ名
#   args4 シート書き込み用の二次元配列[[シート(Sheet1),セル(A1),設定値]]と記載、不要なら[]
##################################################
def callMacroSetCell(dirPath, fileName, macroName, listValue):
	# インスタンス生成
	excel = win32com.client.Dispatch("Excel.Application");

	# エクセルを表示する設定（0にすれば非表示で実行される）
	excel.Visible = 0;

	# ブックを開く
	excel.Workbooks.Open( Filename = dirPath + fileName);

	# 配列があるときだけ処理
	for list in listValue:
		# シートに書き込み
		oSheet = excel.Worksheets(list[0]);
		oSheet.Range(list[1]).value = list[2];

	# マクロ名を実行
	excel.Application.Run(macroName);

	# ブックを保存して閉じる（SaveChangesを0にすると保存せず閉じる）
	excel.Workbooks(1).Close(SaveChanges=1);

	# 終了
	excel.Application.Quit();

##################################################
# メール送信(TEST)
##################################################
def sendMailTest(sendToCcFrom, subject, textL, attachL, removeFlg):
	# 本文に宛先情報を追加
	textData = copy.copy(textL);
	textData.append("To:" + ','.join(sendToCcFrom[0]));
	textData.append("Cc:" + ','.join(sendToCcFrom[1]));
	textData.append("From:" + ','.join(sendToCcFrom[2]));

	sendMail([["takashi.aibara@kubota.com"],["takashi.aibara@kubota.com"],["takashi.aibara@kubota.com"]], "【TEST】" + subject, textData, attachL, removeFlg);

##################################################
# メール送信
#   args1 アドレスの配列、To,Cc,Fromの順に設定
#   args2 メールタイトル
#   args3 メール本文の配列、要素毎に改行
#   args4 添付ファイルのパス配列、空文字は無視
#   args5 Trueなら添付ファイル削除、Falseなら残す
##################################################
def sendMail(sendToCcFrom, subject, textL, attachL, removeFlg):
	msg = MIMEMultipart();

	# Toアドレス
	addressTxt = "";
	for address in sendToCcFrom[0]:
		# 空文字は無視
		if address != "":
			addressTxt = addressTxt + address + ",";
	# Toアドレスをセット
	msg["To"] = addressTxt;
	

	# Ccアドレス
	addressTxt = "";
	for address in sendToCcFrom[1]:
		# 空文字は無視
		if address != "":
			addressTxt = addressTxt + address + ",";
	# Ccアドレスをセット
	msg["Cc"] = addressTxt;

	# Fromアドレス
	addressTxt = "";
	for address in sendToCcFrom[2]:
		# 空文字は無視
		if address != "":
			addressTxt = addressTxt + address + ",";
	# Fromアドレスをセット
	msg["From"] = addressTxt;

	# メールタイトル
	msg["Subject"] = subject;

	# メール本文生成
	message = "";
	for mailText in textL:
		message = message + mailText + "\n";

	# メール本文セット
	msg.attach(MIMEText(message))

	# 添付するファイルを指定
	for path in attachL:
		# 空文字は無視
		if path != "":

			# ファイルがある場合のみ処理
			if os.path.exists(path):
				# ファイルを添付
				with open(path, "rb") as f:
					part = MIMEApplication(f.read(), Name=basename(path));
				part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path);
				msg.attach(part);

				# 削除指定の場合のみ
				if removeFlg:
					#ファイル削除
					os.remove(path)

	# サーバを指定する
	server = smtplib.SMTP("mail.os.ksi.co.jp", 25);
	server.send_message(msg);
	server.quit();

##################################################
# ファイルのコピー
##################################################
def copyFile(dir, srcName, copyName):
	shutil.copyfile(dir + srcName, dir + copyName);

##################################################
# 複数のファイルの存在チェック
##################################################
# 一つでもあればTrueを返す
def existFiles(fileList):
	for path in fileList:
		if path != "":
			if os.path.exists(path):
				return True;
		# 全部ファイルなしならFasle
		return False;

##################################################
# 非稼働日チェックの関数
##################################################
def isNonExecDate():
	dateStr = datetime.datetime.now().strftime('%Y%m%d');
	if dateStr in NonExeDate.NON_EXE_DATE:
		return True;
	else:
		return False;
