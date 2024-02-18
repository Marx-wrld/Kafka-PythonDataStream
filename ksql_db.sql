CREATE TABLE youtube_changes WITH ( KAFKA_TOPIC = 'youtube_changes' ) AS
SELECT 
  video_id,
  latest_by_offset(title) AS title,
  latest_by_offset(comments, 2) [1] AS comments_previous,
  latest_by_offset(comments, 2) [2] AS comments_current,
  latest_by_offset(views, 2) [1] AS views_previous,
  latest_by_offset(views, 2) [2] AS views_current,
  latest_by_offset(likes, 2) [1] AS likes_previous,
  latest_by_offset(likes, 2) [2] AS likes_current
FROM YOUTUBE_VIDEOS 
GROUP BY video_id;


SELECT *
FROM  YOUTUBE_CHANGES
WHERE likes_previous <> likes_current
EMIT CHANGES;


CREATE STREAM telegram_outbox (
  `chat_id` VARCHAR,
  `text` VARCHAR
 ) WITH (
   KAFKA_TOPIC = 'telegram_outbox',
   PARTITIONS = 1,
   VALUE_FORMAT = 'avro'
 );


 INSERT INTO telegram_outbox (
  `chat_id`,
  `text`
) VALUES (
  '811446702',
  'Nearly there!'
);


CREATE STREAM youtube_changes_stream WITH ( KAFKA_TOPIC = 'youtube_changes', VALUE_FORMAT = 'avro');


INSERT INTO telegram_outbox
SELECT 
  '811446702' AS `chat_id`,
  CONCAT(
    'Likes changed: ',
    CAST(likes_previous AS STRING),
    ' => ',
    CAST(likes_current AS STRING),
    '. ',
    title
  ) AS `text`
FROM   YOUTUBE_CHANGES_STREAM 
WHERE likes_current <> likes_previous;