import json

from .MessageUnpack import MsgUnpack
from .MessagePack import MsgPack


def json_to_msgpack(jsonString:str, useFloat=False):
    try:
        obj = json.loads(jsonString)
    except:
        raise "Parse json error."

    pack = MsgPack(useFloat=useFloat)
    return b''.join(pack.object_to_msg_byte(obj))

def msgpack_to_json(msg:bytes):
    if not isinstance(msg, bytes): raise TypeError("Input type should be bytes.")

    unpack = MsgUnpack()
    return json.dumps(unpack.decode_msgpack_bytestring(msg), ensure_ascii=False)