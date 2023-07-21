import random

def ssh_username():
    usernamePath = "ssh_username.txt"
    with open(usernamePath, "r") as user:
        username = user.readlines()
        random.shuffle(username)
        #print(username)
    return username


def ssh_password():
    passwordPath = "ssh_password.txt"
    with open(passwordPath, "rb") as pwd:
        passw = pwd.readlines()
        password = []
        for p in passw:
            pass_ = p.decode("utf8")
            password.append(pass_)
        random.shuffle(password)
        #print(password[-1])
    return password