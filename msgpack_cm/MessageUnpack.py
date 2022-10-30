from collections import defaultdict, deque
import struct

class MsgUnpack:
    
    def __init__(self):
        pass
    
    def decode_msgpack_bytestring(self, msg:bytes):
        if not msg: return None
        self.queue = deque(msg)
        
        return self.decode_msgpack_byte(self.queue.popleft())
    
    def decode_msgpack_byte(self, ele):
        if ele < 0: raise ValueError("Unknown type.")
        elif ele <= 127: return ele

        elif ele <= int('0x8F', 16):
            return self.__to_dict(ele-128)
        
        elif ele <= int('0x9F', 16):
            return self.__to_array(ele- int('0x90', 16))
        
        elif ele <= int('0xBF', 16):
            return self.__to_string(ele-int('0xA0', 16))
        
        elif ele <= int('0xC3', 16):
            if ele == 193: raise ValueError("Never used.")

            codeMap = {192: None, 194: False, 195:True}
            return codeMap[ele]
        
        elif ele <= int('0xC6', 16):
            # bin 8 / 16 / 32
            byte = 2**(ele - int('0xC4', 16))
            size = 0
            for _ in range(byte):
                size = size << 8 | self.queue.popleft()
            
            return self.__to_binary(size)
        
        elif ele <= int('0xC9', 16):
            raise ValueError("Extern reserved.")
        
        elif ele <= int('0xCB', 16):
            # float/32/64
            byte = 4 if ele == int('0xCA', 16) else 8
            return self.__to_float(byte)
        
        elif ele <= int('0xCF', 16):
            # uint8/16/32/64
            byte = 2**(ele-int('0xCC', 16))
            return self.__to_uint(byte)
        
        elif ele <= int('0xD3', 16):
            # int8/16/32/64
            byte = 2**(ele-int('0xD0', 16))

            return self.__to_int(byte)
        
        elif ele <= int('0xD8', 16):
            raise ValueError("Fixext reserved.")
        
        elif ele <= int('0xDB', 16):
            byte = 2**(ele- int('0xD9', 16))
            size = self.__to_uint(byte)
            return self.__to_string(size)
        
        elif ele <= int('0xDD', 16):
            byte = 2 if ele == int('0xDC', 16) else 4
            size = self.__to_uint(byte)

            return self.__to_array(size)
        
        elif ele <= int('0xDF', 16):
            byte = 2 if ele == int('0xDE', 16) else 4
            size = self.__to_uint(byte)

            return self.__to_dict(size)
        
        elif ele <= int('0xFF', 16):
            return -32 + (ele - int('0xE0', 16))
        
        else:
            raise ValueError("Undefined.")


    def __to_dict(self, size):
        res = defaultdict()
        for _ in range(size):
            key = self.decode_msgpack_byte(self.queue.popleft())
            value = self.decode_msgpack_byte(self.queue.popleft())

            if key in res.keys(): raise ValueError("JSON key should be unique.")
            res[key] = value
        
        return res
    
    def __to_array(self, size):
        res = []
        for _ in range(size):
            res.append(self.decode_msgpack_byte(self.queue.popleft()))
        
        return res

    def __to_string(self, size):
        res = []
        for _ in range(size):
            c = self.queue.popleft()
            res.append(int.to_bytes(c, 1, 'big'))
        
        string = str(b"".join(res), 'utf-8')
        
        return string
    
    def __to_binary(self, size):
        res = []
        for _ in range(size):
            ele = self.queue.popleft()
            res.append(ele.to_bytes(1, 'big'))
        
        return b''.join(res)

    def __to_float(self, byte):
        res = 0
        for _ in range(byte):
            res = res<<8 | self.queue.popleft()
        
        ieee754Type = '>f' if byte == 4 else '>d'

        return struct.unpack(ieee754Type, res.to_bytes(byte, 'big'))[0]
    
    def __to_uint(self, byte):
        res = 0
        for _ in range(byte):
            res = res<<8 | self.queue.popleft()
        
        return res
    
    def __to_int(self, byte):
        res = []
        for _ in range(byte):
            res.append(self.queue.popleft().to_bytes(1, 'big'))
        
        return int.from_bytes(b''.join(res), 'big', signed=True)