#!/usr/bin/env python3
# gsm data form
# +CIEV: "MESSAGE",1
# +CMT: "+261348479718",,"2020/12/15,15:39:38+03"
# [12.04/12.16/0.00/0.04/0.00/2393658.25[12.04/1.37/0.00/0.00/0.00/2394985.50[0.00/0.00/0.00/0.00/0.00/0.00[14.13/16.77/0.15/0.00/0.00/2401

# algo process
"""
    read data from monitor serial of arduino
    extract phone number and date and time in data
    extract data report on time
    create file from data in json on the dictionnary temporary (increment name of the file)
"""

import serial
import json
import os
import glob
import uuid

port = '/dev/cu.usbmodemFA131'
baudrate = 9600


def decrypt(value):
    to_decrypt = str(value)
    decrypt_char_lenght = len(to_decrypt)
    k = decrypt_char_lenght
    result = 0
    for item in to_decrypt:
        k = k-1
        result += int(conversion(item)) * pow(35, k)
    return result/100


def conversion(to_decrypt_char):
    switcher = {
        "0": 11,
        "1": 1,
        "2": 17,
        "3": 22,
        "4": 6,
        "5": 13,
        "6": 5,
        "7": 28,
        "8": 3,
        "9": 9,
        "a": 7,
        "b": 10,
        "c": 12,
        "d": 0,
        "e": 15,
        "f": 27,
        "g": 30,
        "h": 2,
        "i": 16,
        "j": 24,
        "k": 4,
        "l": 32,
        "m": 29,
        "n": 23,
        "o": 20,
        "p": 25,
        "q": 26,
        "r": 34,
        "s": 19,
        "t": 31,
        "u": 33,
        "v": 14,
        # "w": 18,
        "x": 18,
        "y": 21,
        "z": 8,
    }
    return str(switcher.get(to_decrypt_char, "Invalid RULES"))


valeur = decrypt("0")
print(valeur)


if __name__ == '__main__':
    ser = serial.Serial(port, baudrate, timeout=1)
    phone_number = "+261xxxxxxxxx"  # save phone number from gsm
    date_of_send = "xxxx/xx/xx"  # save the date when it was published.
    time_of_send = "xx:xx:xx"  # save the time when it was published
    data_on_10_am_slice = "["   # save all data (voltage,current) at 10am
    data_on_12_am_slice = "["    # save all data (voltage,current) at 12am
    data_on_15_pm_slice = "["   # save all data (voltage,current) at 15am
    data_on_17_pm_slice = "["   # save all data (voltage,current) at 17am

    # list of correspondance of phone number and deskName (matching list)
    phone_number_correspondence_list = [
        {"key": "JiroDesk_V2_001", "value": "+261348479718"},
        {"key": "JiroDesk_V2_002", "value": "+261346746200"},
        {"key": "JiroDesk_V2_003", "value": "+261348479720"},
    ]

    # dictionnary for save temporary the json structure
    json_ready_on_dictionary = {}

    print('Established serial connection to Arduino')

    # waiting for a new serial data
    while True:
        try:
            # read serial monitor of arduino and save it
            # arduino_data = ser.readline().decode('utf-8')
            try:
                arduino_data = ser.readline().decode()
                # take only data with +CMT data(phone number, date, time)
                if arduino_data.find('+CMT') != -1:
                    # take only phone number data
                    phone_number = arduino_data.split(
                        '"')[1]
                    # take only date data
                    date_of_send = arduino_data.split('"')[3].split(',')[
                        0]
                    # take only time data
                    time_of_send = arduino_data.split('"')[3].split(',')[
                        1].split(':')[1]
                # take only data with '[' character data (phone number , date , time)
                elif arduino_data.find('[') != -1:
                    # take all data (voltage, current) from 10am
                    data_on_10_am_slice = arduino_data.split('[')[1]
                    # take all data (voltage, current) from 12am
                    data_on_12_am_slice = arduino_data.split('[')[2]
                    # take all data (voltage, current) from 15am
                    data_on_15_pm_slice = arduino_data.split('[')[3]
                    # take all data (voltage, current) from 17am
                    data_on_17_pm_slice = arduino_data.split('[')[4]
                    # check all json file in the current directory
                    nom = glob.glob("*.json")
                    # nom = uuid.uuid1()

                    for c in phone_number_correspondence_list:
                        if c["value"] == phone_number:
                            if data_on_10_am_slice != '[' and data_on_12_am_slice != '[' and data_on_15_pm_slice != '[' and data_on_17_pm_slice != '[':
                                json_ready_on_dictionary[c["key"]] = [
                                    {
                                        "Tension_PV": {
                                            "date": date_of_send,
                                            "time": "10:00",
                                            "valeur": data_on_10_am_slice.split("/")[0]
                                            # "valeur": decrypt(data_on_10_am_slice.split("/")[0])
                                        },
                                        "Tension_Battery":{
                                            "date": date_of_send,
                                            "time": "10:00",
                                            "valeur": data_on_10_am_slice.split("/")[1]
                                            # "valeur": decrypt(data_on_10_am_slice.split("/")[1])
                                        },
                                        "Courant_PV":{
                                            "date": date_of_send,
                                            "time": "10:00",
                                            "valeur": data_on_10_am_slice.split("/")[2]
                                            # "valeur": decrypt(data_on_10_am_slice.split("/")[2])
                                        },
                                        "Courant_Battery":{
                                            "date": date_of_send,
                                            "time": "10:00",
                                            "valeur": data_on_10_am_slice.split("/")[3]
                                            # "valeur": decrypt(data_on_10_am_slice.split("/")[3])
                                        }
                                    },
                                    {
                                        "Tension_PV": {
                                            "date": date_of_send,
                                            "time": "12:00",
                                            "valeur": data_on_12_am_slice.split("/")[0]
                                            # "valeur": decrypt(data_on_12_am_slice.split("/")[0])
                                        },
                                        "Tension_Battery": {
                                            "date": date_of_send,
                                            "time": "12:00",
                                            "valeur": data_on_12_am_slice.split("/")[1]
                                            # "valeur": decrypt(data_on_12_am_slice.split("/")[1])
                                        },
                                        "Courant_PV": {
                                            "date": date_of_send,
                                            "time": "12:00",
                                            "valeur": data_on_12_am_slice.split("/")[2]
                                            # "valeur": decrypt(data_on_12_am_slice.split("/")[2])
                                        },
                                        "Courant_Battery": {
                                            "date": date_of_send,
                                            "time": "12:00",
                                            "valeur": data_on_12_am_slice.split("/")[3]
                                            # "valeur": decrypt(data_on_12_am_slice.split("/")[3])
                                        }
                                    },
                                    {
                                        "Tension_PV": {
                                            "date": date_of_send,
                                            "time": "15:00",
                                            "valeur": data_on_15_pm_slice.split("/")[0]
                                            # "valeur": decrypt(data_on_15_pm_slice.split("/")[0])
                                        },
                                        "Tension_Battery": {
                                            "date": date_of_send,
                                            "time": "15:00",
                                            "valeur": data_on_15_pm_slice.split("/")[1]
                                            # "valeur": decrypt(data_on_15_pm_slice.split("/")[1])
                                        },
                                        "Courant_PV": {
                                            "date": date_of_send,
                                            "time": "15:00",
                                            "valeur": data_on_15_pm_slice.split("/")[2]
                                            # "valeur": decrypt(data_on_15_pm_slice.split("/")[2])
                                        },
                                        "Courant_Battery": {
                                            "date": date_of_send,
                                            "time": "15:00",
                                            "valeur": data_on_15_pm_slice.split("/")[3]
                                            # "valeur": decrypt(data_on_15_pm_slice.split("/")[3])
                                        }
                                    },
                                    {
                                        "Tension_PV": {
                                            "date": date_of_send,
                                            "time": "17:00",
                                            "valeur": data_on_17_pm_slice.split("/")[0]
                                            # "valeur": decrypt(data_on_17_pm_slice.split("/")[0])
                                        },
                                        "Tension_Battery": {
                                            "date": date_of_send,
                                            "time": "17:00",
                                            "valeur": data_on_17_pm_slice.split("/")[1]
                                            # "valeur": decrypt(data_on_17_pm_slice.split("/")[1])
                                        },
                                        "Courant_PV": {
                                            "date": date_of_send,
                                            "time": "17:00",
                                            "valeur": data_on_17_pm_slice.split("/")[2]
                                            # "valeur": decrypt(data_on_17_pm_slice.split("/")[2])
                                        },
                                        "Courant_Battery": {
                                            "date": date_of_send,
                                            "time": "17:00",
                                            "valeur": data_on_17_pm_slice.split("/")[3]
                                            # "valeur": decrypt(data_on_17_pm_slice.split("/")[3])
                                        }
                                    },
                                ]
                    print(json_ready_on_dictionary)
                    # create a data.json file in the same directory of the this current script
                    os.chdir('/Users/MEVA')  # where all file is put
                    with open('data{}.json'.format(str(len(nom))), 'w+') as json_file:
                        json.dump(json_ready_on_dictionary, json_file)
                    json_file.close()
                    print("file creating...")
                    # os.chdir('/Users/MEVA')  # where all file is put
                    # file = open(str(uuid.uuid1()) +
                    #             ".json", "w+")  # name incremented
                    # file.write(
                    #     str(json.dump(json_ready_on_dictionary, fp=file)))
                    # file.close()

                """
                       Process :
                       (i)   Matching phone number and desk name
                       (ii)  Avoid [ caracter
                       (iii) Put on the dictionnary all value from all variables
                    """

            except UnicodeDecodeError:
                print("Encoding error")
        except serial.serialutil.SerialException:
            print("No connection to arduino board!!!")


# def create_files():
#     print("file creating...")
#     os.chdir('/Users/MEVA')  # where all file is put
#     file = open("data" + str(len(nom)) + ".json", "w+")  # name incremented
#     file.write(
#         str(json.dump(json_ready_on_dictionary, fp=file)))
#     file.close()
