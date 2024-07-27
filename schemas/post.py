from datetime import datetime

def serializeDict(item)-> dict:
    return{
        "id": str(item["_id"]),
        "title": item["title"],
        "description": item["description"],
        "created_at": item["created_at"].isoformat() if isinstance(item["created_at"], datetime) else None,
        "updated_at": item["updated_at"].isoformat() if isinstance(item["updated_at"], datetime) else None
    }
    
def serializeList(entity)-> list:
    return [serializeDict(item) for item in entity]