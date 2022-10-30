import struct

class MsgPack:
    
    def __init__(self, useFloat=False):
        self.useFloat = useFloat

    def object_to_msg_byte(self, obj):
        if obj is None: return [b'\xc0']
        
        if isinstance(obj, bool):
            return [b'\xc3'] if obj else [b'\xc2']

        elif isinstance(obj, int):
            return self.int_to_msgType(obj)
        
        elif isinstance(obj, float):
            if self.useFloat: return self.float_to_msgType(obj)
            
            return self.double_to_msgType(obj)

        elif isinstance(obj, str):
            try:
                res = self.str_to_msgType(obj)
            except Exception as e:
                res = self.object_to_msg_byte(None)
                print(f"Parse string error. \n{e}")
            
            return res

        elif isinstance(obj, list):
            return self.array_to_msgType(obj)

        elif isinstance(obj, dict):
            return self.map_to_msgType(obj)
            
        else:
            raise ValueError("Object type error.")

    def int_to_msgType(self, obj:int):
        res = []
        if obj >= 0:
            if obj <= 127:
                return [int.to_bytes(obj, 1, 'big')]

            elif obj <= 2**8 -1:
                res.append(b'\xcc')
                res.append(int.to_bytes(obj, 1, 'big'))

            elif obj <= 2**16-1:
                res.append(b'\xcd')
                res.append(int.to_bytes(obj, 2, 'big'))

            elif obj <= 2**32-1:
                res.append(b'\xce')
                res.append(int.to_bytes(obj, 4, 'big'))

            elif obj <= 2**64-1:
                res.append(b'\xcf')
                res.append(int.to_bytes(obj, 8, 'big'))

            else:
                raise ValueError("Int range error.")
        else:
            # Negative int part
            if obj >= -32:
                return [int.to_bytes(int("0xe0", 16)+ obj-(-32), 1, 'big')]

            elif obj >= -(2**7):
                res.append(b'\xd0')
                res.append(int.to_bytes(obj & (2**8-1), 1, 'big'))

            elif obj >= -(2**15):
                res.append(b'\xd1')
                res.append(int.to_bytes(obj & (2**16-1), 2, 'big'))

            elif obj >= -(2**31):
                res.append(b'\xd2')
                res.append(int.to_bytes(obj & (2**32-1), 4, 'big'))

            elif obj >= -(2**63):
                res.append(b'\xd3')
                res.append(int.to_bytes(obj & (2**64-1), 8, 'big'))

            else:
                raise ValueError("Negative int range error")

        return res

    def map_to_msgType(self, obj:dict):
        res = []
        length = len(obj)
        if length <= 15:
            fixMapSize = int("0x80", 16)+length
            res.append(int.to_bytes(fixMapSize, 1, 'big'))
        
        elif length <= 2**16-1:
            res.extend([
                b'\xde',
                int.to_bytes(length, 2, 'big')
            ])

        elif length <= 2**32-1:
            res.extend([
                b'\xdf',
                int.to_bytes(length, 4, 'big')
            ])
            
        else:
            raise ValueError("Map size error.")
        
        for key, value in obj.items():
                res.extend(self.object_to_msg_byte(key))
                res.extend(self.object_to_msg_byte(value))

        return res

    def str_to_msgType(self, obj:str):
        res = []
        obj = bytes(obj, "utf-8")
        length = len(obj)

        if length <= 31:
            res.append(int.to_bytes(length+int("0xa0", 16), 1, 'big'))

        elif length <= 2**8-1:
            res.append(b'\xd9')
            res.append(int.to_bytes(length, 1, 'big'))

        elif length <= 2**16-1:
            res.append(b'\xda')
            res.append(int.to_bytes(length, 2, 'big'))

        elif length <= 2**32-1:
            res.append(b'\xdb')
            res.append(int.to_bytes(length, 4, 'big'))

        else:
            raise ValueError("String size error.")

        res.append(obj)

        return res

    def float_to_msgType(self, obj:float):
        ieee754Float = struct.unpack('>I',struct.pack('>f',obj))[0]

        return [b'\xca', int.to_bytes(ieee754Float, 4, 'big')]

    def double_to_msgType(self, obj:float):
        ieee754Double = struct.unpack('>Q',struct.pack('>d',obj))[0]

        return [b'\xcb', int.to_bytes(ieee754Double, 8, 'big')]

    def array_to_msgType(self, obj:list):
        length = len(obj)
        res = []
        if length <= 15:
            res.append(int.to_bytes(int("0x90", 16)+length, 1, 'big'))

        elif length <= 2**16-1:
            res.append(b'\xdc')

        elif length <= 2**32-1:
            res.append(b'\xdd')

        else:
            raise ValueError("Array size error.")
        
        for ele in obj:
            res.extend(self.object_to_msg_byte(ele))
        
        return res