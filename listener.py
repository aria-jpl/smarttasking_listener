import json
from datetime import datetime

def get_querysince(delta):
    return(datetime.utcnow() - timedelta(hours=delta)).strftime('%Y-%m-%dT%H:%M:%S')