import hashlib


class Block:

    def __init__(self, timestamp, pre_block_hash='', transactions=None):
        """
        区块类的构造函数

        Parameters:
            timestamp (str): 区块的时间戳
            pre_block_hash (str): 前一个区块的哈希值，默认为空字符串
            transactions (list): 交易列表，默认为空列表

        Attributes:
            pre_block_hash (str): 前一个区块的哈希值
            timestamp (str): 区块的时间戳
            transactions (list): 交易列表
            merkle_root_hash (str): 交易列表的默克尔根哈希值
            nonce (int): 工作量证明的随机数
            hash (str): 区块的哈希值
        """
        if transactions is None:
            transactions = []
        self.pre_block_hash = pre_block_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root_hash = self.transactions_hash(transactions)
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        计算区块的哈希值

        Returns:
            str: 计算得到的区块的哈希值
        """
        # 将区块信息拼接然后生成哈希值
        block_str = str(self.pre_block_hash) + str(self.timestamp) + self.merkle_root_hash + str(self.nonce)
        # 选择哈希函数（此处使用SHA-256）
        hash_func = hashlib.sha256()
        hash_func.update(block_str.encode())
        hash = hash_func.hexdigest()
        return hash

    @staticmethod
    def transactions_hash(transactions):
        """
        计算交易列表的默克尔根哈希值

        Parameters:
            transactions (list): 交易列表

        Returns:
            str: 计算得到的默克尔根哈希值
        """
        arr_str = ''.join(str(element) for element in transactions)
        return hashlib.sha256(arr_str.encode()).hexdigest()