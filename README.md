# Face_recognition_opens_the_door
人脸识别自动开门  
基于dlib库的shape_predictor_68_face_landmarks.dat训练模型  
利用arduino uno r3进行控制  
# 文件树
```
│  run.py
│  shape_predictor_68_face_landmarks.dat
│  sketch_sep23a.ino
│
└─face
        xxx.jpg
        xxx.jpg
        xxx.jpg
```
**run.py为主程序**  
**sketch_sep23a.ino为单片机程序**  
**face为存放已知人脸文件夹**  
# uno r3连接引脚方法
我这里用到了红灯和绿灯用来提示门锁状态  
红灯亮起为门锁紧闭  
绿灯亮起为门锁开启  
```
const int RedLed = 5;    //红灯5引脚
const int GreenLed = 6;  //绿灯6引脚
const int Spin = 9;      //舵机9引脚
```
**其他线自行连接**
# 主要构思
python处理图像，如果多次识别成功就串口发送给单片机
