import requests
import os
import re
from datetime import datetime

def plex_curr_version():
    rpm_output = os.system('rpm -qa | grep plex')
    plex_curr = re.findall("\d+\.\d+\.\d+\.\d+", rpm_output)
    return plex_curr[0]

def download_plex_json():
    URL = 'https://plex.tv/api/downloads/5.json'
    r = requests.get(URL)
    if r.status_code != 200:
        raise Exception
    return r.json()

def number_of_objects_in_json(res_json):
    return len(res_json)

def convert_download_to_json(res_json, length):
    dic = {}
    for i in range(0, length):
        for key, item in res_json.items():
            if key not in dic.keys():
                dic[key] = []
            dic[key].append(item)
    return dic

def find_loc_centos_item(dic):
    distro = 'centos'
    arch = '64'

    for key, value in dic.items():
        if key == 'label':
            for item in value:
                if distro in item.lower() and arch in item.lower():
                    loc = value.index(item)
    return loc

def find_url_centos(location):
    for key, value in dic.items():
        if key == 'url':
            url = value[loc]
    return url

def download_latest_rpm(url):
    home = '/home/tabac/'
    r = requests.get(url, allow_redirects=True)
    save_loc = os.path.join(home, 'new_plex.rpm')
    open(save_loc, 'wb').write(r.content)
    return save_loc

def get_local_curr_plex():
    plex_curr = os.popen('rpm -qa | grep plex').read()
    #plex_curr = 'plexmediaserver-1.19.5.3112-b23ab3896.x86_64\n'
    match = re.findall("\d+\.\d+\.\d+\.\d+", plex_curr)
    return match[0]

def get_plex_remote_ver(res_json):
    for item in res_json['computer']['Linux'].items():
        if item[0] == 'version':
            remote_ver = item[1]
    plex_curr_remote = re.findall("\d+\.\d+\.\d+\.\d+", remote_ver)
    return plex_curr_remote[0]

def run_rpm(rpm):
    os.system('sudo yum -y install {}'.format(rpm))

def del_rpm(rpm):
    os.system('rm {}'.format(rpm))

def write_to_log(log_file, state, version):
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    with open(log_file, 'a+') as f: 
        if state == 'success':
            f.write('{} - Installed new version: {}\n'.format(current_time, version))
        else:
            f.write('{} - No changes\n'.format(current_time))

def main():
    log_file = '/home/tabac/plex_log'
    plex_total_json = download_plex_json()
    plex_links_json = plex_total_json['computer']['Linux']['releases']
    plex_remote_ver = get_plex_remote_ver(plex_total_json)
    local_plex_ver = get_local_curr_plex()
    if plex_remote_ver > local_plex_ver:
        len_of_json = number_of_objects_in_json(plex_links_json)
        download_sorted_dic = convert_download_to_json(plex_links_json, len_of_json)
        loc = find_loc_centos_item(download_sorted_dic)
        centos_url = find_url_centos(loc)
        download_location = download_latest_rpm(centos_url)
        run_rpm(download_location)
        del_rpm(download_location)
        write_to_log(log_file, 'success', plex_remote_ver)
    else:
        write_to_log(log_file, 'no_update', 0)


if __name__ == '__main__':
    main()