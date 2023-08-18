from Block import Block
from BlockChain import BlockChain
from Miner import Miner
import time

from Transaction import Transaction


def mine_block(block_chain, mine):
    """
       挖掘新的区块并将其添加到区块链中。

       Parameters:
           block_chain (BlockChain): 区块链实例
           mine (Miner): 矿工实例

       Returns:
           None
    """
    # 添加初块奖励
    transaction = Transaction(sender=None, recipient=mine.account_address, amount=block_chain.mining_reward)
    block_chain.add_transaction(transaction)

    # 创建区块
    pre_block_hash = block_chain.get_latest_block().hash
    new_block = Block(timestamp=time.time(), pre_block_hash=pre_block_hash,
                      transactions=block_chain.pending_transactions)

    # 开始挖矿
    time_start = time.perf_counter()
    # 要求hash值前difficulty个位为0
    while new_block.hash[0: block_chain.difficulty] != ''.join(['0'] * block_chain.difficulty):
        # 不符合要求
        new_block.nonce += 1
        new_block.timestamp = time.time()
        new_block.hash = new_block.calculate_hash()

    time_end = time.perf_counter()
    print("挖到区块:{0}, 耗时: {1}秒".format(new_block.hash,time_end-time_start))
    block_chain.add_block(new_block)




if __name__ == '__main__':
    timestamp = time.time()
    block_chain = BlockChain(timestamp)

    # 创建矿工mine1，mine2
    miner1 = Miner("xuxiaoyang")
    miner2 = Miner("zhangshan")

    mine_block(block_chain=block_chain, mine=miner1)
    print("用户名：{0}\n账户：{1} \n余额：${2}".format(miner1.unique_no, miner1.account_address,
                                                   block_chain.get_balance_by_address(miner1.account_address)))

    transaction = Transaction(miner1.account_address, miner2.account_address, 500)
    block_chain.add_transaction(transaction)
    mine_block(block_chain=block_chain, mine=miner2)
    print("用户名：{0}\n账户：{1} \n余额：{2}".format(miner2.unique_no, miner2.account_address,
                                                   block_chain.get_balance_by_address(miner2.account_address)))

    print("当前区块链长{0}".format(len(block_chain.chain)))



