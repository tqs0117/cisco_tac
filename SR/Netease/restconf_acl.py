#!/usr/bin/env python3

import requests
import json
import datetime

payload_raw = "{\n  \"Cisco-IOS-XE-acl:access-list-seq-rule\": {\n    " \
          "\"sequence\": \"1100\",\n    \"ace-rule\": {\n      " \
          "\"action\": \"permit\",\n      \"protocol\": \"ip\",\n      " \
          "\"any\": [\n        null\n      ],\n      \"dst-host\": \"101.246.84.86\"\n    " \
          "}\n  }\n}"
payload_dict = json.loads(payload_raw)


def create_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step):
    with open('script.log', 'a+') as log:
        log.write(str(datetime.datetime.now()) + '\n')
        log.write('Starting to create acl from seq {} to {} by step of {}..\n\n'.format(
            acl_start_seq, acl_stop_seq, acl_seq_step))

    for acl_seq in range(acl_start_seq, acl_stop_seq, acl_seq_step):
        # modify acl parameters to json payload
        payload_dict["Cisco-IOS-XE-acl:access-list-seq-rule"]["sequence"] = str(acl_seq)
        payload_dict["Cisco-IOS-XE-acl:access-list-seq-rule"]["ace-rule"]["dst-host"] = "10.1.{}.{}".format(
            acl_seq // 256, acl_seq % 256)

        payload = json.dumps(payload_dict)

        url = "https://{}/restconf/data/Cisco-IOS-XE-native:native/ip" \
              "/access-list/extended=\"{}\"/access-list-seq-rule={}".format(
            ip_addr, acl_name, acl_seq)

        headers = {
            'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json',
            'Authorization': 'Basic Y2lzY286Y2lzY28='
        }

        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)

        print(response.text.encode('utf8'))

    with open('script.log', 'a+') as log:
        log.write(str(datetime.datetime.now()) + '\n')
        log.write('Completed to create acl from seq {} to {} by step of {} :)\n\n'.format(
            acl_start_seq, acl_stop_seq, acl_seq_step))


def patch_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step):
    with open('script.log', 'a+') as log:
        log.write(str(datetime.datetime.now()) + '\n')
        log.write('Starting to patch acl from seq {} to {} by step of {}..\n\n'.format(
            acl_start_seq, acl_stop_seq, acl_seq_step))

    for acl_seq in range(acl_start_seq, acl_stop_seq, acl_seq_step):
        # modify acl parameters to json payload
        payload_dict["Cisco-IOS-XE-acl:access-list-seq-rule"]["sequence"] = str(acl_seq)
        payload_dict["Cisco-IOS-XE-acl:access-list-seq-rule"]["ace-rule"]["dst-host"] = "10.2.{}.{}".format(
            acl_seq // 256, acl_seq % 256)
        payload = json.dumps(payload_dict)

        url = "https://{}/restconf/data/Cisco-IOS-XE-native:native/ip" \
              "/access-list/extended=\"{}\"/access-list-seq-rule={}".format(
            ip_addr, acl_name, acl_seq)

        headers = {
            'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json',
            'Authorization': 'Basic Y2lzY286Y2lzY28='
        }

        response = requests.request("PATCH", url, headers=headers, data=payload, verify=False)

        print(response.text.encode('utf8'))

    with open('script.log', 'a+') as log:
        log.write(str(datetime.datetime.now()) + '\n')
        log.write('Completed to patch acl from seq {} to {} by step of {} :)\n\n'.format(
            acl_start_seq, acl_stop_seq, acl_seq_step))


def delete_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step):
    with open('script.log', 'a+') as log:
        log.write(str(datetime.datetime.now()) + '\n')
        log.write('Starting to delete acl from seq {} to {} by step of {}..\n\n'.format(
            acl_start_seq, acl_stop_seq, acl_seq_step))

    for acl_seq in range(acl_start_seq, acl_stop_seq, acl_seq_step):
        payload = {}

        url = "https://{}/restconf/data/Cisco-IOS-XE-native:native/ip" \
              "/access-list/extended=\"{}\"/access-list-seq-rule={}".format(
            ip_addr, acl_name, acl_seq)

        headers = {
            'Content-Type': 'application/yang-data+json',
            'Accept': 'application/yang-data+json',
            'Authorization': 'Basic Y2lzY286Y2lzY28='
        }

        response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)

        print(response.text.encode('utf8'))

    with open('script.log', 'a+') as log:
        log.write(str(datetime.datetime.now()) + '\n')
        log.write('Completed to delete acl from seq {} to {} by step of {} :)\n\n'.format(
            acl_start_seq, acl_stop_seq, acl_seq_step))


def test_loop1(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step, iteration):
    if iteration == 0:
        while True:
            with open('script.log', 'a+') as log:
                log.write(str(datetime.datetime.now()) + '\n')
                log.write('Starting test_loop1..\n\n')

            create_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step)
            patch_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step)
            delete_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step)

            with open('script.log', 'a+') as log:
                log.write(str(datetime.datetime.now()) + '\n')
                log.write('Completed test_loop1!! :)\n\n')
    else:
        i = 0
        while i < iteration:
            with open('script.log', 'a+') as log:
                log.write(str(datetime.datetime.now()) + '\n')
                log.write('Starting test_loop1 iteration {}..\n\n'.format(i))

            create_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step)
            patch_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step)
            delete_acl(ip_addr, acl_name, acl_start_seq, acl_stop_seq, acl_seq_step)

            with open('script.log', 'a+') as log:
                log.write(str(datetime.datetime.now()) + '\n')
                log.write('Completed test_loop1 ineration {}!! :)\n\n'.format(i))

            i = i + 1


# Entry point for program
if __name__ == '__main__':
    test_loop1("10.106.38.156", "NAM", 1500, 1600, 1, 0)

