import os

#os.system(f'pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu')
with open('requirements.txt', 'r') as f:
    for line in f.readlines():
        os.system(f'python -m pip install --upgrade --no-cache-dir --use-deprecated=legacy-resolver {line}')
os.system('sudo apt-get install libmysqlclient-dev -y')
os.system('python3 -m pip install mysqlclient')
'''
kobert tokenizer : https://vhrehfdl.tistory.com/148 참조
'''

