import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from os.path import basename

##################################################
# メール送信
#   args1 アドレスの配列、To,Cc,Fromの順に設定
#   args2 メールタイトル
#   args3 メール本文の配列、要素毎に改行
#   args4 添付ファイルのパス配列、空文字は無視
#   args5 Trueなら添付ファイル削除、Falseなら残す
##################################################
def sendMailHtml(sendToCcFrom, subject, textL, attachL, removeFlg):
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
    if addressTxt != "":
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
    msg.attach(MIMEText(message, "html"))

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
                    # ファイル削除
                    os.remove(path)

    # サーバを指定する
    server = smtplib.SMTP("mail.os.ksi.co.jp", 25);
    server.send_message(msg);
    server.quit();



mailTextHtml = [\
"<html>"
"<body>"
"<table>"
"  <tr><td>a</td><td>b</td><td>c</td></tr>"
"  <tr><td>1</td><td>2</td><td>3</td></tr>"
"</table>"
"<body>"
"</html>"
]

sendMailHtml([["takashi.aibara@kubota.com"],[],["takashi.aibara@kubota.com"]], "HTMLテスト", mailTextHtml, [], True)
