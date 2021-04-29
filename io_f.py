# -*- coding: utf-8-unix -*-

import re
from dataclasses import dataclass
import numpy as np

@dataclass
class ReadData:
    startTime   : int
    endTime     : int
    acce        : np.ndarray
    acce_uncali : np.ndarray
    gyro        : np.ndarray
    gyro_uncali : np.ndarray
    magn        : np.ndarray
    magn_uncali : np.ndarray
    ahrs        : np.ndarray
    wifi        : np.ndarray
    ibeacon     : np.ndarray
    waypoint    : np.ndarray

re_LINE_HEADER = re.compile('\\d{13}\tTYPE_')
def to_logical_lines(line):
    mutch_list = list(re.finditer(re_LINE_HEADER, line))
    assert(len(mutch_list) > 0)
    index_list = [m.start() for m in mutch_list] + [len(line)]
    logical_lines = (line[index_list[i]:index_list[i+1]] for i in range(len(index_list)-1))
    for logical_line in logical_lines:
        yield logical_line
    return

def read_data_file(data_filename):
    acce = list()
    acce_uncali = list()
    gyro = list()
    gyro_uncali = list()
    magn = list()
    magn_uncali = list()
    ahrs = list()
    wifi = list()
    ibeacon = list()
    waypoint = list()
    startTime = None
    endTime   = None

    with open(data_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith('#\tstartTime'):
            startTime = int(re.split('[:\t]', line)[2])
            continue
        if line.startswith('#\tendTime'):
            endTime = int(re.split('[:\t]', line)[2])
            continue
        if (not line) or line.startswith('#'):
            continue
        for line_data in to_logical_lines(line):
            line_data = line_data.split('\t')

            if line_data[1] == 'TYPE_ACCELEROMETER':
                acce.append([int(line_data[0]), float(line_data[2]), float(line_data[3]), float(line_data[4])])
                continue

            if line_data[1] == 'TYPE_ACCELEROMETER_UNCALIBRATED':
                if len(line_data) > 5:
                    acce_uncali.append([int(line_data[0]),
                                        float(line_data[2]), # x
                                        float(line_data[3]), # y
                                        float(line_data[4]), # z
                                        float(line_data[5]), # x
                                        float(line_data[6]), # y
                                        float(line_data[7]), # z
                                        int(  line_data[8]), # accuracy
                                        ])
                else:
                    acce_uncali.append([int(line_data[0]),
                                        float(line_data[2]), # x
                                        float(line_data[3]), # y
                                        float(line_data[4]), # z
                                        ])
                continue

            if line_data[1] == 'TYPE_GYROSCOPE':
                gyro.append([int(line_data[0]), float(line_data[2]), float(line_data[3]), float(line_data[4])])
                continue

            if line_data[1] == 'TYPE_GYROSCOPE_UNCALIBRATED':
                if len(line_data) > 5:
                    gyro_uncali.append([int(line_data[0]),
                                        float(line_data[2]), # x
                                        float(line_data[3]), # y
                                        float(line_data[4]), # z
                                        float(line_data[5]), # x
                                        float(line_data[6]), # y
                                        float(line_data[7]), # z
                                        int(  line_data[8]), # accuracy
                                        ])
                else:
                    gyro_uncali.append([int(line_data[0]),
                                        float(line_data[2]), # x
                                        float(line_data[3]), # y
                                        float(line_data[4]), # z
                                        ])
                continue

            if line_data[1] == 'TYPE_MAGNETIC_FIELD':
                magn.append([int(line_data[0]), float(line_data[2]), float(line_data[3]), float(line_data[4])])
                continue

            if line_data[1] == 'TYPE_MAGNETIC_FIELD_UNCALIBRATED':
                if len(line_data) > 5:
                    magn_uncali.append([int(line_data[0]),
                                        float(line_data[2]), # x
                                        float(line_data[3]), # y
                                        float(line_data[4]), # z
                                        float(line_data[5]), # x
                                        float(line_data[6]), # y
                                        float(line_data[7]), # z
                                        int(  line_data[8]), # accuracy
                                        ])
                else:
                    magn_uncali.append([int(line_data[0]),
                                        float(line_data[2]), # x
                                        float(line_data[3]), # y
                                        float(line_data[4]), # z
                                        ])
                continue

            if line_data[1] == 'TYPE_ROTATION_VECTOR':
                ahrs.append([int(line_data[0]), float(line_data[2]), float(line_data[3]), float(line_data[4])])
                continue

            if line_data[1] == 'TYPE_WIFI':
                sys_ts = line_data[0]
                ssid = line_data[2]
                bssid = line_data[3]
                rssi = line_data[4]
                lastseen_ts = line_data[6]
                wifi_data = [sys_ts, ssid, bssid, rssi, lastseen_ts]
                wifi.append(wifi_data)
                continue

            if line_data[1] == 'TYPE_BEACON':
                ts = line_data[0]
                uuid = line_data[2]
                major = line_data[3]
                minor = line_data[4]
                rssi = line_data[6]
                ibeacon_data = [ts, '_'.join([uuid, major, minor]), rssi]
                ibeacon.append(ibeacon_data)
                continue

            if line_data[1] == 'TYPE_WAYPOINT':
                waypoint.append([int(line_data[0]), float(line_data[2]), float(line_data[3])])
                continue

    acce = np.array(acce)
    acce_uncali = np.array(acce_uncali)
    gyro = np.array(gyro)
    gyro_uncali = np.array(gyro_uncali)
    magn = np.array(magn)
    magn_uncali = np.array(magn_uncali)
    ahrs = np.array(ahrs)
    wifi = np.array(wifi)
    ibeacon = np.array(ibeacon)
    waypoint = np.array(waypoint)

    return ReadData(startTime, endTime, acce, acce_uncali, gyro, gyro_uncali, magn, magn_uncali, ahrs, wifi, ibeacon, waypoint)
