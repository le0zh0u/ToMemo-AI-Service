import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        return json.JSONEncoder.default(self, obj)