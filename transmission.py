#!/usr/bin/env python

import rospy
import socket
from sensor_msgs.msg import Range, NavSatFix, Image
from std_msgs.msg import String, Float32

UDP_IP = "192.168.1.100"  # Alamat IP mikrokontroler STM32
UDP_PORT = 12345  # Port yang digunakan untuk komunikasi UDP
PASSWORD = "ITS"  # Password yang digunakan (ganti sesuai kebutuhan)

def lidar_callback(data):
    # Mengirim data jarak dari LIDAR ke mikrokontroler STM32 melalui UDP
    send_udp_data(str(data.range))

def gps_callback(data):
    # Mengirim data posisi dari GPS ke mikrokontroler STM32 melalui UDP
    send_udp_data(str(data.latitude))
    send_udp_data(str(data.longitude))

def pixhawk_callback(data):
    # Mengirim data kemiringan dari Pixhawk ke mikrokontroler STM32 melalui UDP
    send_udp_data(data.data)

def camera_callback(data):
    # Mengirim data gambar dari kamera ke mikrokontroler STM32 melalui UDP
    # Kode implementasi tergantung pada format gambar yang digunakan
    # Gantilah dengan implementasi yang sesuai untuk mengirim data gambar

    # Contoh kode dummy untuk mengirim informasi gambar
    send_udp_data("Gambar diterima")

def mode_callback(data):
    # Mengirim data mode (manual atau autonomous) ke mikrokontroler STM32 melalui UDP
    send_udp_data(data.data)

def pid_callback(data):
    # Mengirim data PID ke mikrokontroler STM32 melalui UDP
    send_udp_data(str(data.data))

def send_udp_data(data):
    # Mengecek password sebelum mengirimkan data ke mikrokontroler STM32 melalui UDP
    password = PASSWORD + UDP_IP[:3]  # Mengambil 3 digit pertama alamat IP
    if password == "ITS" + UDP_IP[:3]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
        sock.close()
    else:
        rospy.logwarn("Password tidak valid")

if _name_ == '_main_':
    rospy.init_node('ethernet_udp_sender_node')

    # Subscriber untuk menerima data jarak dari LIDAR
    rospy.Subscriber('lidar_range', Range, lidar_callback)

    # Subscriber untuk menerima data posisi dari GPS
    rospy.Subscriber('gps_position', NavSatFix, gps_callback)

    # Subscriber untuk menerima data kemiringan dari Pixhawk
    rospy.Subscriber('pixhawk_tilt', String, pixhawk_callback)

    # Subscriber untuk menerima data gambar dari kamera
    rospy.Subscriber('camera_image', Image, camera_callback)

    # Subscriber untuk menerima data mode (manual atau autonomous)
    rospy.Subscriber('mode', String, mode_callback)

    # Subscriber untuk menerima data PID
    rospy.Subscriber('pid_data', Float32, pid_callback)

    rospy.spin()