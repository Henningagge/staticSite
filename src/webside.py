import os
import os.path
import shutil


def makePulic():
    path_to_check = "public"
    if os.path.exists(path_to_check):
        try:
            shutil.rmtree(path_to_check)
            os.mkdir(path_to_check)
        except :
            print("could not create directory")
    else:
        try:
            os.mkdir(path_to_check)
        except :
            print("could not create directory")
    rekusionCopy("static")

def rekusionCopy(path):
    print(path)
   
    dirList = []
    entries = os.listdir(path)
    for entry in entries:
        if os.path.isfile(f"{path}/{entry}"):
            try:
                shutil.copy(f"{path}/{entry}",f"public/{path[6:]}")

            except:
                print("error was not a file")

        else:
            try:

                os.mkdir(f"public/{entry}")
            except :
                print("could not create directory")
            dirList.append(f"{path}/{entry}")
    print(dirList)
    print("!!!!!!!!!!")
    for dirpath in dirList:
        rekusionCopy(dirpath)