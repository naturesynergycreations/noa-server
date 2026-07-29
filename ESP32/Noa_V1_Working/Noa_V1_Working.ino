#include <WiFi.h>
#include <driver/i2s.h>
#include <HTTPClient.h>

String serverURL = "http://192.168.1.11:5000/upload";
//==================== WIFI ====================

const char* ssid = "Airtel_shan_6791";
const char* password = "Air@90242";

//==================== BOOT BUTTON ====================

#define BUTTON_PIN 18

//==================== INMP441 ====================

#define I2S_WS   5
#define I2S_SD   6
#define I2S_SCK  4

//==================== SPEAKER ====================

#define SPK_BCLK 16
#define SPK_LRC  17
#define SPK_DOUT 15

String replyURL = "http://192.168.1.11:5000/reply";

#define SAMPLE_RATE 16000

bool recording = false;
#define RECORD_SECONDS 4

int16_t *audioBuffer = NULL;

const int TOTAL_SAMPLES = SAMPLE_RATE * RECORD_SECONDS;

void micInit();
void speakerInit();
void playReply();

void uploadAudio()
{
  WiFiClient client;
HTTPClient http;

client.setTimeout(10000);

http.begin(client, serverURL);
http.setTimeout(10000);

http.addHeader("Content-Type", "application/octet-stream");

int httpResponseCode = http.POST(
    (uint8_t*)audioBuffer,
    TOTAL_SAMPLES * sizeof(int16_t)
);

Serial.print("HTTP Response : ");
Serial.println(httpResponseCode);

if (httpResponseCode > 0)
{
    Serial.println(http.getString());
}

http.end();

delay(500);

speakerInit();
playReply();
micInit();

}

void micInit();
void speakerInit();
void playReply();

void setup() {

  Serial.begin(115200);

  // ---------- Button ----------
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // ---------- WiFi ----------
  Serial.println();
  Serial.print("Connecting WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.print("IP : ");
  Serial.println(WiFi.localIP());

  micInit();
  
  Serial.println();
  Serial.println("Press BOOT button...");
  
  audioBuffer = (int16_t *)ps_malloc(TOTAL_SAMPLES * sizeof(int16_t));

if (audioBuffer == NULL) {
  Serial.println("PSRAM Allocation Failed!");
  while (1);
}

Serial.println("PSRAM Ready");
}

void loop() {

  if (digitalRead(BUTTON_PIN) == LOW) {

    delay(50);

    if (digitalRead(BUTTON_PIN) == LOW) {

      Serial.println("Recording...");

      int32_t sample32;
      size_t bytesRead;

      for (int i = 0; i < TOTAL_SAMPLES; i++) {

        i2s_read(
          I2S_NUM_0,
          &sample32,
          sizeof(sample32),
          &bytesRead,
          portMAX_DELAY
        );

        audioBuffer[i] = sample32 >> 15;
      }

      Serial.println("Recording Finished");

      Serial.print("Recorded Samples : ");
      Serial.println(TOTAL_SAMPLES);
      uploadAudio();

      while (digitalRead(BUTTON_PIN) == LOW);

      delay(500);
    }
  }
}
void micInit()
{
    static bool firstTime = true;

    if (!firstTime)
    {
        i2s_driver_uninstall(I2S_NUM_0);
    }

    firstTime = false;

    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 512,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };

    i2s_pin_config_t pin_config = {
        .bck_io_num = I2S_SCK,
        .ws_io_num = I2S_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = I2S_SD
    };

    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config);
    i2s_zero_dma_buffer(I2S_NUM_0);

    Serial.println("Microphone Ready");
}
void speakerInit()
{
  i2s_driver_uninstall(I2S_NUM_0);

  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 512,
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = SPK_BCLK,
    .ws_io_num = SPK_LRC,
    .data_out_num = SPK_DOUT,
    .data_in_num = I2S_PIN_NO_CHANGE
  };

  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
  i2s_zero_dma_buffer(I2S_NUM_0);

  Serial.println("Speaker Ready");
}
void playReply()
{
  WiFiClient client;
  HTTPClient http;

  Serial.println("Downloading reply.wav...");

  http.begin(client, replyURL);

  int code = http.GET();

  if (code != HTTP_CODE_OK)
  {
    Serial.println("Download Failed");
    http.end();
    return;
  }

  WiFiClient *stream = http.getStreamPtr();

  // Skip WAV header
  for (int i = 0; i < 44; i++)
    stream->read();

  uint8_t buffer[1024];

  while (http.connected() || stream->available())
  {
    int available = stream->available();

    if (available > 0)
    {
      int len = stream->readBytes(buffer, min(available, 1024));

      int16_t *samples = (int16_t *)buffer;

      for (int i = 0; i < len / 2; i++)
      {
        int32_t s = samples[i] * 3;

        if (s > 32767) s = 32767;
        if (s < -32768) s = -32768;

        samples[i] = (int16_t)s;
      }

      size_t written;

      i2s_write(
        I2S_NUM_0,
        buffer,
        len,
        &written,
        portMAX_DELAY
      );
    }

    delay(1);
  }

  http.end();

  Serial.println("Playback Finished");
  delay(300);
}

