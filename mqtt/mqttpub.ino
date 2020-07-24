#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define MAX_MSG_LEN (128)
const char* ssid = "NETGEAR504";
const char* password = "1qaz@WSX";
//const char* serverHostname = "rpi4b";
const IPAddress serverIPAddress(10,0,0,11); 
const char* topic = "jufeng/awsl";
WiFiClient espClient;
PubSubClient client(espClient);

void connectWifi(){
  delay(10);
  Serial.printf("\nConnecting to %s\n", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected on IP Address ");
  Serial.println(WiFi.localIP());
}
void connectMQTT(){
  while(!client.connected()){
    String clientId = "ESP8266-";
    clientId += String(random(0xffff),HEX);
    Serial.printf("MQTT connecting as client %s...\n", clientId.c_str());
    //Attempt to connect
    if(client.connect(clientId.c_str())){
      Serial.println("MQTT connected");
      client.publish(topic, "hello from ESP8266");
      client.subscribe(topic);
      
    }else{
      Serial.printf("MQTT failed, state %s, retrying ...\n",client.state());
      delay(2500);
    }
  }
}

void callback(char *msgTopic, byte* msgPayload, unsigned int msgLength){
  static char message[MAX_MSG_LEN+1];
  if(msgLength > MAX_MSG_LEN){
    msgLength = MAX_MSG_LEN;
  }
  strncpy(message, (char*)msgPayload, msgLength);
  message[msgLength] = '\0';
  Serial.printf("topic %s, message received: %s\n",msgTopic, message);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  connectWifi();
  client.setServer(serverIPAddress, 1883);
  client.setCallback(callback);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!client.connected()){
    connectMQTT();
  }
//  Serial.print("ADC Value: ");
  int ana = analogRead(A0);
  //Serial.println(ana);//读取A0脚的数据，输出0-1023 对应 外部输入电压 0-1.0v
  client.publish(topic, String(ana).c_str());
  client.loop();
  delay(1000);
}
