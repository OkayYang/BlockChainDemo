import hashlib
class Transaction:
    def __init__(self, sender, recipient, amount):
        """
        交易类的构造函数

        Parameters:
            sender (str): 发送者的地址
            recipient (str): 接收者的地址
            amount (float): 交易金额

        Attributes:
            sender (str): 发送者的地址
            recipient (str): 接收者的地址
            amount (float): 交易金额
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def calculate_hash(self):
        """
        计算交易的哈希值

        Returns:
            str: 计算得到的交易的哈希值
        """
        transaction_data = self.sender + self.recipient + str(self.amount)
        return hashlib.sha256(transaction_data.encode()).hexdigest()