import os
import sys

userName="ansible"


def allocateRights():

    os.system("echo \""+userName+"  ALL=(ALL)   NOPASSWD: ALL\" >> /etc/sudoers")


def addUser():

    passwd="012345789!!"
    # Create user
    # -u UID
    # -U create group with same name as user
    # 
    os.system("useradd -c AnsibleUser \
            -u 5000 \
            -U \
            -s /bin/bash \
            -p"+passwd+" "+userName)


if __name__ == '__main__':
    addUser()
    allocateRights()
