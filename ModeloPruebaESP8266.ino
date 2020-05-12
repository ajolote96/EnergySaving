#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

///Variables globales
float irms = 0.00;
int voltaje = 0;
float watts = 0.00;
float intensidadPico = 0.00;
 
///variables globales de frran
float Sensibilidad = 0.100;
int Ruido = 0;
const int SensorIntencidad = A0;
float ValorReposo = 2.50;
float tensionDeRed = 230.0;
int x = 5;

///credenciales de wifi
const char *ssid = "Francisco2_plus";
const char *password = "FranCisC0@113";

//Definiciones de pin
#define RelayPin     2

 
ESP8266WebServer server(80);
 
void setup(void) 
{
   Serial.begin(115200);
   
   //wifi setup
   Wifi();

   //iniciarmos las rutas y el servidor
   RutasDeServidor();
   server.begin();
   Serial.println("HTTP server started");

   //instanciamos el relay
   pinMode(RelayPin, OUTPUT);
}
 
void loop()
{
   AlmacenarValores();
   server.handleClient();
   Http();
}
 
void Wifi() {
  Serial.println();
  Serial.println();
  Serial.print("conectando a ");
  Serial.println(ssid);
  //WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("*****************************************************");
  }

void Http(){
  HTTPClient http;
  //127.0.0.1:8000/RecivirData/?irms=10&voltaje=10&watts=25&intensidadPico=10
  http.begin("http://192.168.0.8:8000/RecivirData/?irms=" + String(irms) + "&voltaje=" + String(voltaje) + "&watts=" + String(watts) + "&intensidadPico=" + String(intensidadPico));
  int httpCode = http.GET();
 
  if (httpCode > 0) {
    String payload = http.getString();
    Serial.println(payload);
  }else{
    Serial.println("No se pudo conectar al servidor.");
  }
 
  http.end();   //Close connection
  }

void RutasDeServidor(){
    // Ruteo para '/'
   server.on("/", []() {
      server.send(200, "text/plain", "Hola mundo!");
   });
 
   // Ruteo para '/inline' usando función lambda
   server.on("/inline", []() {
      server.send(200, "text/plain", "Esto tambien funciona");
   });

   // Ruteo para encender
   server.on("/encender", [](){
      server.send(200);
    });

      // Ruteo para encender
   server.on("/apagar", [](){
      server.send(200);
    });
 
   // Ruteo para URI desconocida
   server.onNotFound([](){
      server.send(404, "text/plain", "Not found");
    });
  }

float LeerCorriente(){
  float ValorVoltajeSensor;
  float Corriente = 0;
  long Tiempo = millis();
  float IntensidadMaxima = 0;
  float IntensidadMinima = 0;
  while(millis() - Tiempo < 500){
    ValorVoltajeSensor = analogRead(SensorIntencidad) * (5.0 / 1023.0);
    Corriente = 0.9 * Corriente + 0.1 * ((ValorVoltajeSensor - ValorReposo)/ Sensibilidad);
    
    if(Corriente > IntensidadMaxima)
      IntensidadMaxima = Corriente;
    if(Corriente < IntensidadMinima)
      IntensidadMinima = Corriente;
    }
  return(((IntensidadMaxima - IntensidadMinima)/2)-Ruido);
}

void AlmacenarValores(){

  irms = 0.00;
  voltaje = 0;
  watts = 0.00;
  intensidadPico = 0.00;

  for(cont=0; cont < 60; cont++){
    intensidadPico = LeerCorriente();
    voltaje = (25.0 * analogRead(x)/1023) * 5;
    irms = intensidadPico * 0.707;
    watts = watts + (irms * voltaje);
    delay(999);//casi un segundo jajaja 
  }
}
