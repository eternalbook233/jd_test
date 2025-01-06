import redis

# 创建一个连接到 Redis 服务器的连接对象
# 如果 Redis 服务器在不同的主机上，请提供相应的主机和端口参数
# 如果有密码认证，使用 password 参数提供密码
redis_client = redis.StrictRedis(
    host='wtet.site',
    port=6379,
    password='Qq233333',
    decode_responses=True
)


# 不要在这里关闭连接

def get_redis(name):
    value = redis_client.get(name)
    return int(value) if value is not None else 1


def set_redis(name, value):
    return redis_client.set(name, value)


if __name__ == '__main__':
    # 在此处执行您的 Redis 操作
    result = get_redis('example_key')
    print(result)

# 在程序结束时关闭连接
redis_client.close()
