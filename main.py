# pip install pandas
# pip install pandas
# pip install pandas


import yaml
import requests
import pandas as pd
pd.options.display.max_colwidth = 150

with open ('params.yaml', 'r', encoding='UTF-8') as f:
    params = yaml.safe_load(f)

login = params['login']
password = params['password']
login_url = params['login_url']
common_file_link_url_prefix = params['common_file_link_url_prefix']
common_file_link_url_postfix = params['common_file_link_url_postfix']
file_list = params['file_list']
folder_path = params['folder_path']
input_file = params['input_file']
input_full_path = folder_path + input_file

data = {"Login":login, "Password":password, "_csrf_token":"undefined"} #

df = pd.read_excel(input_full_path)
file_list = df['Название файла результата'].str.strip().tolist()
print('\nfile_list = \n', file_list)

check_response = requests.get(url=login_url, data=data)
if int(check_response.status_code) != 200:
    print('что-то с авторизацией.status_code =', check_response.status_code)
else:
    print('c авторизацией все ок. status_code =', check_response.status_code)

    session = requests.Session()
    session.post(url=login_url, data=data)

    #print('посмотрим на куки', session.cookies.get_dict()) # print('посмотрим на куки', session.cookies.get_dict())

    for file in range(len(file_list)):
        print('file =', file_list[file])
        full_path = folder_path + str(file_list[file])
        print('full_path =', full_path)
        file_link_url = common_file_link_url_prefix + str(file_list[file]) + common_file_link_url_postfix
        print('file_link_url =', file_link_url)

        response = session.get(url=file_link_url) #, cookies =session.cookies

        with open(full_path, 'wb') as output:
            output.write(response.content)
