import time
import threading

# 打印缓冲区锁
# print buffer lock
print_lock = threading.Lock()

class Singleton():
    _instance_lock = threading.Lock()

    def __init__(self):
        time.sleep(1)
        pass

    @classmethod
    def instance(cls):
        Singleton._instance_lock.acquire()
        if not hasattr(Singleton, "_instance"):
            Singleton._instance = Singleton()
        Singleton._instance_lock.release()
        return Singleton._instance


def task():
    # 必须通过.instance()进行创建单例实例,直接Singleton创建的并不是单例模式
    # you should create instance by "Single.instance()" instead of "Singleton()"
    obj = Singleton.instance()

    print_lock.acquire()
    print obj
    print_lock.release()

for i in range(10):
    t = threading.Thread(target=task)
    t.start()