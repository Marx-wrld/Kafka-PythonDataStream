from typing import Dict
config: Dict[str, str] = {
    "google_api_key": "AIz...",
    "youtube_playlist_id": "PLF...",
    "kafka": {
        "bootstrap.servers": "pkc...",
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "PLAIN",
        "sasl.username": "...",
        "sasl.password": "...",
    },
    "schema_registry": {
        "url": "https://...",
        "basic.auth.user.info": "...",
    }
}