import hashlib

class Miner:
    def __init__(self, unique_no):
        """
        矿工类的构造函数

        Parameters:
            unique_no (str): 矿工的唯一编号,要具有伪随机性确保唯一避免产生碰撞

        Attributes:
            unique_no (str): 矿工的唯一编号
            _private_key (str): 私钥
            public_key (str): 公钥
            account_address (str): 账户地址
        """
        self.unique_no = unique_no

        # 生成私钥
        self._private_key = hashlib.sha256(unique_no.encode()).hexdigest()

        # 根据私钥生成公钥
        self.public_key = hashlib.sha256(self._private_key.encode()).hexdigest()

        # 根据公钥生成账户地址
        self.account_address = hashlib.sha256(self.public_key.encode()).hexdigest()