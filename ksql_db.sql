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