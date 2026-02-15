// presage_gsr_sender.ino
// Reads GSR sensor and sends JSON data over Serial

const int GSR_PIN = A0;
const int SENSOR_THRESHOLD = 50; // Filter out noise when not worn

void setup() {
  // 115200 is fast enough for low-latency data
  Serial.begin(115200); 
}

void loop() {
  int gsrValue = analogRead(GSR_PIN);
  
  // Only send data if someone is actually wearing it (approximate)
  // or just send everything and let Python filter it.
  
  // Format: {"happiness": -1, "gsr": 512}
  // We use happiness: -1 so the Python script knows this is BIO data, not FACE data.
  Serial.print("{\"happiness\": -1, \"gsr\": ");
  Serial.print(gsrValue);
  Serial.println("}");
  
  delay(50); // 20 times per second (20Hz)
}