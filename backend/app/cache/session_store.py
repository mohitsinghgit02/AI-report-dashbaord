import uuid

sessions = {}


def create_session(data):

    ref_key = str(uuid.uuid4())

    sessions[ref_key] = data

    return ref_key


def get_session(ref_key):

    return sessions.get(ref_key)
