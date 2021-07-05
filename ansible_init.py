import os
import sys

def checkArgvNum():
    num = len(sys.argv)

    if num < 2 :
        print("인자 값이 없습니다")
    else :
        for i in range(1, len(sys.argv)) :
            print("{}번째 인자 값 {}".format(i,sys.argv[i]))

        makeDir(sys.argv[1])


def makeDir(absPath):
    path = ['/inventory', '/playbooks', '/roles']
    
    try :
        os.mkdir(absPath)

    except FileNotFoundError as e :
        print(e)

    except FileExistsError as e :
        print(e)


    finally :
        for i in range(len(path)) :
            os.makedirs(absPath + path[i], exist_ok=True)





checkArgvNum()
