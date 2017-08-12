# 测试Cache Aside Pattern在高并发下cache与db不一致的问题

- 首先启动server.py，它会自动清除redis中的缓存
- 接着启动client.py即可还原场景
