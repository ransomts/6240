#!/usr/bin/env python3
# an example entry:
#   /home/tsranso/.emacs.d/Maildir/tsranso/Automated/security information/cur/1586536789.200676_9487.tengen,U=1092:2,S:joey4.computing.clemson.edu : Feb 21 21:04:33 : etichen : user NOT in sudoers ; TTY=pts/13 ; PWD=/home/etichen/cpsc2100 ; USER=root ; COMMAND=/usr/bin/apt install sublime-text



import pprint
import re
from string import digits

logs = raw.split("\n")

def make_report (logs):
    def install_request_in_log(log):
        return 'install' in log["command"]
    install_logs = list(filter(install_request_in_log, logs))
    num_install_requests = len(install_logs)
    #print(install_logs)
    print(F"total logs:", (len(logs)))
    print(F"requests for installs:", (num_install_requests))
    print()

    def global_requested_packages(logs):
        def pull_command(log):
            command = ''
            try:
                command = log["command"].split("install")[1].strip()
            except:
                command = ''
            return command

        requested_packages = sorted(list(map(pull_command , logs)))
        for rp in requested_packages:
            if " " in rp:
                requested_packages.remove(rp)
                for p in rp.split(' '):
                    requested_packages.append(p)
        requested_packages = list(filter(None, requested_packages))
        package_counts = [[x,requested_packages.count(x)] for x in set(requested_packages)]

        print("Most requested logs, and how many times they were asked for:")
        print(sorted(package_counts, key=lambda x : x[1])[-6:])
        print()

    print("Most requested packages for all machines")
    global_requested_packages(logs)

    remove_digits = str.maketrans('', '', digits)
    for machine in set(map(lambda x : x["machine"].split(".")[0].translate(remove_digits), install_logs)):
        print("Most requested packages for machine class", machine)
        global_requested_packages(list(filter(lambda x : machine in x["machine"], install_logs)))

    def get_user_stats (logs):
        user_counts = [[user, len(list(filter(lambda x : x["user"] == user, logs)))] for user in set(map(lambda log : log["user"], logs))]
        print("Users with high sudo failures, maybe email them?")
        high_failure_users = list(filter(lambda user_entry : user_entry[1] > 10, sorted(user_counts, key=lambda x : x[1])))
        print(high_failure_users)
        
    get_user_stats(logs)

def processLog(log):
    splitLog = re.split(':|;', log)
    logDict = {}
    try:
        logDict = {
            'command' : splitLog[11].split('=')[1].lower(),
            'date' : F"{splitLog[3]}:{splitLog[4]}:{splitLog[5]}".strip(),
            'user' : splitLog[6].strip(),
            'machine' : splitLog[2].strip(),
            'pwd' : splitLog[9].split('=')[1].strip()
        }
        #        print('good dict')
    except:
        logDict = {}
        #        print('bad dict')
    return logDict

# processed = pool.map(processLog,logs)
# print('yay')
# pprint.pprint(processed[0:3])
processed = list()
for log in logs:
    #pprint.pprint(processLog(log))
    pl = processLog(log)
    if pl:
        processed.append(pl)
        #print(pl)
        #        print(f'{processLog(log)["user"]} {processLog(log)["command"]}')
# print(processed)
make_report(processed)
