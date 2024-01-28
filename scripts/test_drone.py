import keyboard
import airsim

client = airsim.MultirotorClient()
client.confirmConnection()

def abc(x:keyboard.KeyboardEvent):
    w = keyboard.KeyboardEvent('down', 28, 'w')
    s = keyboard.KeyboardEvent('down', 28, 's')
    a = keyboard.KeyboardEvent('down', 28, 'a')
    d = keyboard.KeyboardEvent('down', 28, 'd')
    up = keyboard.KeyboardEvent('down', 28, 'up')
    down = keyboard.KeyboardEvent('down', 28, 'down')
    left = keyboard.KeyboardEvent('down', 28, 'left')
    right = keyboard.KeyboardEvent('down', 28, 'right')
    enter = keyboard.KeyboardEvent('down', 28, 'enter')
    k = keyboard.KeyboardEvent('down', 28, 'k')
    l = keyboard.KeyboardEvent('down', 28, 'l')
    if x.event_type == 'down' and x.name == w.name:
        #前進
        client.moveByVelocityBodyFrameAsync(3, 0, 0, 0.5)  # 控制無人機x正方向移動，不等待完成

        print("你按下了 "+ x.name + " 鍵")
    elif x.event_type == 'down' and x.name == s.name:
        #後退
        client.moveByVelocityBodyFrameAsync(-3, 0, 0, 0.5)

        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == a.name:
        #左移
        client.moveByVelocityBodyFrameAsync(0, -2, 0, 0.5)
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == d.name:
        #右移
        client.moveByVelocityBodyFrameAsync(0, 2, 0, 0.5)
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == up.name:
        #上升
        client.moveByVelocityBodyFrameAsync(0, 0, -0.5, 0.5)
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == down.name:
        #下降
        client.moveByVelocityBodyFrameAsync(0, 0, 0.5, 0.5)
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == left.name:
        #左轉
        client.rotateByYawRateAsync(-20, 0.5)
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == right.name:
        #右轉
        client.rotateByYawRateAsync(20, 0.5)
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == enter.name:
        #enter
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == k.name:
        # 獲得控制
        client.enableApiControl(True)
        print("獲得控制")
        # 解鎖
        client.armDisarm(True)
        print("解鎖")
        client.takeoffAsync().join()
        print("起飛")
        print("你按下了 " + x.name + " 鍵")
    elif x.event_type == 'down' and x.name == l.name:
        #降落
        client.landAsync().join()
        print("降落")
        # 上鎖
        client.armDisarm(False)
        print("上鎖")
        # 釋放控制
        client.enableApiControl(False)
        print("釋放控制")

        print("你按下了 " + x.name + " 鍵")
    else:  # 沒有按下按鍵
        client.moveByVelocityBodyFrameAsync(0, 0, 0, 0.5).join()
        client.hoverAsync().join()  # 第四階段：懸停6秒鐘
        print("停止 懸停")

# 當監聽的事件為enter鍵，且是按下的時候
keyboard.hook(abc)
keyboard.wait()