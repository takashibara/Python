import os

#複数のファイルの存在チェック
#一つでもあればTrueを返す
def existFiles(fileList):
    for path in fileList:
        if path != "":
            if os.path.exists(path):
                return True;
    #全部ファイルなしならFasle
    return False;

files = [ \
"C:/bootsqmaa.dat",
"C:/bootsqm.dat",
""];

if existFiles(files):
    print("ファイルあり");
else:
    print("ファイルなし");
