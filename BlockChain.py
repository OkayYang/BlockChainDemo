from Block import Block
import time

from Transaction import Transaction


class BlockChain:
    def __init__(self, timestamp):
        """
        区块链类的构造函数

        Parameters:
            timestamp (str): 创世区块的时间戳

        Attributes:
            chain (list): 区块链列表
            difficulty (int): 工作量证明的难度
            pending_transactions (list): 待处理交易列表
            mining_reward (float): 挖矿奖励
        """
        # 给创始人账户记录100000000￥
        genesis_block = Block(timestamp, transactions=[Transaction('', '0001', 100000000)])

        # 区块链
        self.chain = [genesis_block]
        # 待处理的交易列表
        self.pending_transactions = []
        # 挖矿难度
        self.difficulty = 5
        # 出块奖励
        self.mining_reward = 1000

    def add_transaction(self, transaction):
        """
        添加待处理交易

        Parameters:
            transaction (Transaction): 待处理的交易对象
        """

        # 判断是否为出块奖励
        if transaction.sender is not None:
            print("账户{0}向账户{1}发起一笔${2}的转账交易。".format(transaction.sender,transaction.recipient,transaction.amount))
            sender_balance = self.get_balance_by_address(transaction.sender)
            if transaction.amount<sender_balance:
                self.pending_transactions.append(transaction)
            else:
                print("{0}的账户余额不足,可用资金为${1}！".format(transaction.sender,sender_balance))
        else:
            self.pending_transactions.append(transaction)

    def get_latest_block(self):
        """
        获取最新的区块

        Returns:
            Block: 最新的区块对象
        """
        return self.chain[-1]

    def get_balance_by_address(self, address):
        """
        根据地址获取余额

        Parameters:
            address (str): 地址

        Returns:
            float: 地址对应的余额
        """
        balance = 0
        for block in self.chain:
            for trans in block.transactions:
                # 账户支出
                if trans.sender == address:
                    balance -= trans.amount
                # 账户收入
                if trans.recipient == address:
                    balance += trans.amount
        return balance

    def add_block(self, new_block):
        """
        添加新的区块到区块链中

        Parameters:
            new_block (Block): 要添加的新区块

        Returns:
            bool: 新区块是否成功添加到区块链中
        """
        # 验证区块是否合法
        if self.is_valid_block(new_block):
            self.chain.append(new_block)
            self.pending_transactions = []
            return True
        else:
            return False

    def is_valid_block(self, new_block):
        """
        验证新区块的合法性

        Parameters:
            new_block (Block): 要验证的新区块

        Returns:
            bool: 新区块是否合法
        """
        current_block = self.get_latest_block()

        # 验证新区块的哈希值是否正确
        if new_block.hash != new_block.calculate_hash():
            print("该区块非法，内容被篡改!")
            return False

        # 验证新区块的前一个区块哈希值是否正确
        if new_block.pre_block_hash != current_block.calculate_hash():
            print("该区块非法，不是最长合法链!")
            return False

        # 验证新区块的工作量证明是否满足要求
        if not self.is_valid_proof(new_block, self.difficulty):
            print("该区块非法，工作量证明不足!")
            return False

        print("恭喜你获得出块奖励${0}!".format(self.mining_reward))
        return True

    def is_valid_proof(self, block, difficulty):
        """
        验证区块的工作量证明是否满足要求

        Parameters:
            block (Block): 要验证的区块
            difficulty (int): 工作量证明的难度

        Returns:
            bool: 区块的工作量证明是否满足要求
        """
        target = '0' * difficulty
        return block.hash[:difficulty] == target