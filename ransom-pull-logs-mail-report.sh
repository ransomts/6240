/bin/bash
db_file=/home/tsranso/sudo-logs/log-db.cur
tims_password=not_really_my_password

if [ -f $db_file ]; then
    cat log-db* > log-db-archive
fi

function ask_machines() {
    for i in $(seq 1 18); do ssh ada$i     "echo $tims_password | sudo -S grep 'sudo' /var/log/auth.log* 2>/dev/null"; done
    for i in $(seq 1 35); do ssh babbage$i "echo $tims_password | sudo -S grep 'sudo' /var/log/auth.log* 2>/dev/null"; done
    for i in $(seq 1 21); do ssh joey$i    "echo $tims_password | sudo -S grep 'sudo' /var/log/auth.log* 2>/dev/null"; done
    for i in $(seq 1 20); do ssh cerf$i    "echo $tims_password | sudo -S grep 'sudo' /var/log/auth.log* 2>/dev/null"; done
    for i in $(seq 1 5);  do ssh titan$i   "echo $tims_password | sudo -S grep 'sudo' /var/log/auth.log* 2>/dev/null"; done
}

function add_logs_to_db () {
    ask_machines | grep -e 'user NOT in sudoers' -e 'install' >> $db_file
}

add_logs_to_db

mail -s 'sudo report' tsranso@clemson.edu < $(python3 parse-sudo-db.py)
