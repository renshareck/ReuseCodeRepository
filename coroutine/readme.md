#关于python中协程、多线程理解

======================================================================

##强调 python中多线程实质并未用到多核

==================================

##协程

通过代码逻辑级别或者编译器级别对程序逻辑进行调整优化，以实现在主动地在不同模块方法之间调用切换，减少无谓的上下文切换消耗


##多线程

借由系统安排，对正在执行的各个线程中内容进行一定的调度（譬如按时间片轮询），以实现并发，但需要消耗部分系统资源进行调度上下文切换等


##协程、多线程与阻塞io

实际上，单纯的协程并不能用在io密集型操作之上，因为单纯的协程的io操作是阻塞性的。

譬如利用协程爬取多个网站。在协程中将访问网站并爬取其内容作为一个原子操作，分析内容作为另一个原子操作。于是其它协程的操作（爬取下一个网站内容）都会被阻塞于此。

但多线程并不存在爬取下个网站内容被阻塞，因为这些线程是轮询进行的。


##协程、多线程与非阻塞io、异步io、事件驱动io、io多路复用

协程若要在io密集型操作中达到多线程的效果，就必须解决阻塞io的问题。


非阻塞io：  若io未准备好或其他原因而无法立即完成，则先返回其它结果

异步io：    个人认为最好的方式，提交io操作后由其它部件进行io操作，本身可以进行其他任务，io部件完成后返回完成信号

事件驱动io：基于事件驱动模型而实现的io处理机制

io多路复用：针对io操作额外再进行多线程或者其它等类似的轮询处理io操作

