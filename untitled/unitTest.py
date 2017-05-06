import unittest


# 单元测试是用来对一个模块、一个函数或者一个类来进行正确性检验的测试工作。
# 比如对函数abs()，我们可以编写出以下几个测试用例：
#     输入正数，比如1、1.2、0.99，期待返回值与输入相同；
#     输入负数，比如-1、-1.2、-0.99，期待返回值与输入相反；
#     输入0，期待返回0；
#     输入非数值类型，比如None、[]、{}，期待抛出TypeError。
# 把上面的测试用例放到一个测试模块里，就是一个完整的单元测试。
# 我们来编写一个Dict类，这个类的行为和dict一致，但是可以通过属性来访问，用起来就像下面这样：
# >>> d = Dict(a=1, b=2)
# >>> d['a']
# 1
# >>> d.a
# 1

class Dict(dict):
    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s" % key)

    def __setattr__(self, key, value):
        self[key] = value


# unittest Dict
class TestDict(unittest.TestCase):
    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty

    # 可以在单元测试中编写两个特殊的setUp()
    # 和tearDown()
    # 方法。这两个方法会分别在每调用一个测试方法的前后分别被执行。
    #
    # setUp()
    # 和tearDown()
    # 方法有什么用呢？设想你的测试需要启动一个数据库，这时，就可以在setUp()
    # 方法中连接数据库，在tearDown()
    # 方法中关闭数据库，这样，不必在每个测试方法中重复相同的代码：
    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')


if __name__ == '__main__':
    unittest.main()
