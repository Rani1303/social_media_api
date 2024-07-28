def serializeSaveDict(save) -> dict:
    return {
        "id": str(save["_id"]),
        "user_id": save["user_id"],
        "post_id": save["post_id"],
        "created_at": save["created_at"]
    }

def serializeSaveList(saves) -> list:
    return [serializeSaveDict(save) for save in saves]