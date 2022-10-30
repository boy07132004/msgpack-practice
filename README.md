# Msgpack

## What is MessagePack?

MessagePack is an efficient binary serialization format. It lets you exchange data among multiple languages like JSON. But it's faster and smaller. Small integers are encoded into a single byte, and typical short strings require only one extra byte in addition to the strings themselves.

## What is this repo for?

This repo is a project for converting format between JSON string and MessagePack.

## How to use it?

```python
import msgpack_cm
msgPackOutput = msgpack_cm.json_to_msgpack('{"input": "the JSON string"}')
jsonStringOutput = msgpack_cm.msgpack_to_json('''msgpack byte string''')
```

> The default float type is IEEE 754 double precision. If you need IEEE 754 single precision, use `msgpack_cm.json_to_msgpack('{"input": "the JSON string"}', useFloat=True)` instead.
> 

## Limitation

"Ext type" and "Timestamp type" are not defined since JSON isn't supported.