## Kafka-PythonDataStream

Turning a static data source—YouTube’s REST API—into a reactive system that:

- Uses Python to fetch and process data from a static web API
- Streams that data live, from Python into a Kafka topic
- Processes the incoming source data with ksqlDB, watching for important changes
- Then streams out live, custom notifications via Telegram
  
### Project Installation

> Clone or download the project, then get API keys from [Kafka Confluent](https://login.confluent.io/login?state=hKFo2SBOeVdmSjZKbl9aNE04bjdRZGk3V0VieHRLakNqU3Q2YaFupWxvZ2luo3RpZNkgRWFOQlVvTER2QS1OV0Y3TmZ4T0NOSXYzZjFaUnZ4TEijY2lk2SBsMmhPcDBTMHRrU0IwVEZ0dklZZlpaOUVhS0Z2clNjNg&client=l2hOp0S0tkSB0TFtvIYfZZ9EaKFvrSc6&protocol=oauth2&cache=%5Bobject%20Object%5D&redirect_uri=https%3A%2F%2Fconfluent.cloud%2Fauth_callback&redirect_path=%2F&last_org_resource_id_map=%7B%22e1e225b4cdfec4f00cf73f67d4aed929cf92a4af195f0b6ad05d3939626b2d78%22%3A%7B%22org_resource_id%22%3A%223b7b68ba-2a9a-4a70-94b5-e7402dc7f9e7%22%2C%22timestamp%22%3A1708102812057%2C%22is_sso%22%3Afalse%7D%7D&segment_anon_id=eae06838-e73f-4552-8815-5cf380a7c74f&scope=openid%20profile%20email%20offline_access&response_type=code&response_mode=query&nonce=Ylo1VWJheHVQRWlDYkRLUmhiZ3FVVVMuUXNZZ0NlelVjWEc3cEYwRS00Ng%3D%3D&code_challenge=2KG-s8d56DGtcxFO8TZ_C-T3vPItAa2L1227-aDaxM0&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtcmVhY3QiLCJ2ZXJzaW9uIjoiMS4xMi4xIn0%3D)

#### Create virtualenv
```
virtualenv venv
```

#### Activate the virtual environment
- source venv/bin/activate - Linux
- venv/Scripts/activate - Windows

#### Install the required packages
pip install -r requirements.txt

#### Run the application
```
python app.py
```
#### Deactivate the virtual environment
```
deactivate
```
