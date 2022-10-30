import msgpack
import json
import msgpack_cm

test = ['{"null":null}', '{"int":[0, 127, 128, 255, 256, 65535, 65536]}', \
    '{"int2":{"a": 2147483647, "b":2147483648, "c":4294967295} }', \
    '{"nint":[-1, -32, -33, -128, -256, -32768, -65536, -2147483648]}', \
    '{"float": [0.5, -0.5]}', '{"big num": 18446744073709551615, "big nnum": -9223372036854775808 }', \
    '{"array": [[], {"nested": [{}]}]}', '{"bolean": [true, false]}', \
     '{"emoji1": "❤", "🍺": "emoji2"}'
]

for idx in range(len(test)):
    myFunc      = msgpack_cm.json_to_msgpack(test[idx])
    # print(f"         {myFunc}")
    pkgFunc  = msgpack.packb(json.loads(test[idx]))
    # print(f"         {pkgFunc}")
    print(idx, end=" ")

    myJsonString = msgpack_cm.msgpack_to_json(myFunc)
    pkgJson= msgpack.unpackb(pkgFunc)

    if pkgFunc == myFunc and json.loads(myJsonString) == pkgJson:
        print("pass")
    else:
        print("failed")