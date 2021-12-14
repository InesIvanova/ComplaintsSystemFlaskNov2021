import base64

from werkzeug.exceptions import BadRequest

from models import State

state_query_mapper = {
    "pending": State.pending,
    "approved": State.approved,
    "rejected": State.rejected,
}


def decode_photo(encoded_photo, path):
    try:
        with open(path, "wb") as file:
            file.write(base64.b64decode(encoded_photo.encode("utf-8")))
    except Exception:
        raise BadRequest("Invalid photo")


def process_query_filters(filters):
    if "status" in filters:
        filters["status"] = state_query_mapper.get(filters["status"].lower())
    if "amount" in filters:
        filters["amount"] = float(filters["amount"])
    return filters
