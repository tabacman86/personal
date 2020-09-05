#!/usr/bin/python3
import requests
import os
import re
from datetime import datetime
import logging

logger = logging
logger.basicConfig(filename='/home/tabac/plex_log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logger.INFO)

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
    print(length)
    print(res_json)
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

def find_url_centos(response):
    distro = 'centos'
    arch = '64'
    for item in response:
        if distro in item['label'].lower() and arch in item['label'].lower():
            url = item['url']
            logger.info('Got URL of new version')
    return url

    # for key, value in dic.items():
    #     if key == 'url':
    #         url = value[loc]
    return url

def download_latest_rpm(url):
    home = '/home/tabac/'
    r = requests.get(url, allow_redirects=True)
    save_loc = os.path.join(home, 'new_plex.rpm')
    logger.info('Downloading new version')
    open(save_loc, 'wb').write(r.content)
    return save_loc

def get_local_curr_plex():
    plex_curr = os.popen('rpm -qa | grep plex').read()
    #plex_curr = 'plexmediaserver-1.19.5.3112-b23ab3896.x86_64\n'
    match = re.findall("\d+\.\d+\.\d+\.\d+", plex_curr)
    logger.info('Plex local version: {}'.format(plex_curr))
    return match[0]

def get_plex_remote_ver(res_json):
    for item in res_json['computer']['Linux'].items():
        if item[0] == 'version':
            remote_ver = item[1]
    plex_curr_remote = re.findall("\d+\.\d+\.\d+\.\d+", remote_ver)
    logger.info('Plex remote version: {}'.format(plex_curr_remote))
    return plex_curr_remote[0]

def run_rpm(rpm):
    logger.info('Installing new version')
    os.system('sudo yum -y install {}'.format(rpm))

def del_rpm(rpm):
    os.system('rm {}'.format(rpm))

def write_tologger(log_file, state, version):
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    with open(log_file, 'a+') as f:
        if state == 'success':
            f.write('{} - Installed new version: {}\n'.format(current_time, version))
        else:
            f.write('{} - No changes\n'.format(current_time))

def main():
    log_file = '/home/tabac/plexlogger'
    plex_total_json = download_plex_json()
    plex_links_json = plex_total_json['computer']['Linux']['releases']
    plex_remote_ver = get_plex_remote_ver(plex_total_json)
    local_plex_ver = get_local_curr_plex()
    if plex_remote_ver > local_plex_ver:
        logger.info('Found new version: {}'.format(plex_remote_ver))
        centos_url = find_url_centos(plex_links_json)
        download_location = download_latest_rpm(centos_url)
        run_rpm(download_location)
        del_rpm(download_location)
        logger.info('Version {} installed successfully'.format(plex_remote_ver))
    else:
        logger.info('No new version')

if __name__ == '__main__':
    main()
