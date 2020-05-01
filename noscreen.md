
# 没显示器也玩树莓派全攻略
树莓派4B支持了双屏幕显示
但是如果不用显示器的话
却要增加一些设置才能愉快玩耍

今天我们就演示一遍在没有显示器的情况下
从装系统到远程桌面连接成功
都需要做哪些事情

## 1 烧录系统镜像
官网下载镜像文件， 然后用Etcher烧录进TF卡
## 2 预埋wifi和sh
1，新建wpa_supplicant.conf，放入boot盘

    country=CN
    ctrl_interface=DIR=/var/run/wpa_supplicant
    update_config=1
    
    network={
        ssid="WiFi-A”//wifi名字
        psk=“12345678”//密码
        key_mgmt=WPA-PSK
    }
2，新建ssh空文件，放入boot盘
## 3 插电启动，用fing找到ip
## 4 ssh连接树莓派
进入raspi-config完成
1，先改个密码，
2，设置vnc开启，
3，设置分辨率

再设置静态ip
修改/etc/dhcpcd.conf
添加你指定的ip地址和路由器
## 5 使用vnc远程桌面