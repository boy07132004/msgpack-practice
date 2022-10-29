# Msgpack

## What is MessagePack?

MessagePack is an efficient binary serialization format. It lets you exchange data among multiple languages like JSON. But it's faster and smaller. Small integers are encoded into a single byte, and typical short strings require only one extra byte in addition to the strings themselves.

## What is this repo for?

This repo is a project for converting format between JSON string and MessagePack.

## How to use it?

```python
from MessagePack import MsgPack
pack = MsgPack()
pack.jsonString_to_pack('{"input": "the JSON string"}')
```

> The default float type is IEEE 754 double precision. If you need IEEE 754 single precision, use `pack = MsgPack(useFloat=True)` instead.
> 

## Future

- MessagePack back to JSON string