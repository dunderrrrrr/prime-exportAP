# prime-exportAP
Export accesspoint data from Cisco Prime API.

Best used with virtualenv like below.
```
mkvirtualenv --python=/usr/bin/python3 prime-exportAP
```

## Installation
`git clone git@github.com:dunderrrrrr/prime-exportAP.git`  

Then install requirements with pip.
```
pip install -r requirements.txt
```
Edit exportAP.py
```
prime_server = 'http://prime.domain.com' #prime url
prime_user = 'user_read' #prime user with read permissions
prime_passwd = 'user_passwd' #prime user passwd
* Add/remove data in def format_apdata() for custom export fields
```
Run script with args

```
$ python exportAP.py --aplist list.txt
['FDW0000ABCD', 'APName_01', 'AP', 'AP', 'Cisco', 'AIR-AP2802I-E-K9', '00:00:00:00:00:00']
['FDW0001ABCD', 'APName_02', 'AP', 'AP', 'Cisco', 'AIR-AP2802I-E-K9', '00:00:00:00:00:01']
['APName_03 not found in Prime!']
Exporting csv...
Done, exported csv: /home/user/dev/prime-exportAP/output_2019-02-21_10-26-24.csv
```

```
$ cat output_2019-02-21_10-26-24.csv
FDW0000ABCD,APName_01,AP,AP,Cisco,AIR-AP2802I-E-K9,00:00:00:00:00:00
FDW0001ABCD,APName_02,AP,AP,Cisco,AIR-AP2802I-E-K9,00:00:00:00:00:01
APName_03 not found in Prime!
```
