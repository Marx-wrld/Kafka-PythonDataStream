## Kafka-PythonDataStream

Turning a static data source—YouTube’s REST API—into a reactive system that:

- Uses Python to fetch and process data from a static web API
- Streams that data live, from Python into a Kafka topic
- Processes the incoming source data with ksqlDB, watching for important changes
- Then streams out live, custom notifications via Telegram
