#include <Servo.h>

// 设置引脚和创建对象
const int RedLed = 5;
const int GreenLed = 6;
const int Spin = 9;
int start = 0;
Servo MySpin;

// 基础设置
void setup()
{
  // 设置比特率
  Serial.begin(9600);
  // 设置输出端口
  pinMode(RedLed, OUTPUT);
  pinMode(GreenLed, OUTPUT);
  // 让红灯开始时亮，让绿灯开始时灭
  digitalWrite(RedLed, HIGH);
  digitalWrite(GreenLed, LOW);
  // 赋予舵机对象,转到0
  MySpin.attach(Spin, 544, 2500);
  MySpin.write(0);
  delay(15);
}

// 舵机控制部分
void spin()
{
  MySpin.write(180);
  delay(15000);
  MySpin.write(0);
}

// 主程序
void loop()
{
  while (true)
  {
    // 当有信号的时候
    // if(start == 4)
    // {
    //   start == 0;
    //   Serial.begin(9600);
    // }
    if(Serial.available() > 0 )
    {
      char ch = Serial.read();
      // 传过来的是1
      switch(ch)
      {
        case '1':
        {
          digitalWrite(RedLed,LOW);
          digitalWrite(GreenLed,HIGH);
          start += 1;
          spin();
          digitalWrite(GreenLed,LOW);
          digitalWrite(RedLed,HIGH);
          break;
        }
      // if(start == 4)
      // {
      //   Serial.end();
      //   break;
      // }
      }
    }
  }
}
