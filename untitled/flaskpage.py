# -*- coding: utf-8 -*-
from flask import Flask, render_template
import bars

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index-simple.html',
                           datas=bars.datas,
                           dates=bars.dates,
                           fenbi=bars.fenbi)


# route() 装饰器用于把一个函数绑定到一个 URL 。 下面是一些基本的例子:
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# 通过把 URL 的一部分标记为 <variable_name> 就可以在 URL 中添加变量。标记的 部分会作为关键字参数传递给函数。通过使用 <converter:variable_name> ，可以 选择性的加上一个转换器，为变量指定规则。请看下面的例子:
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')  # 转换器： int  float  path
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


# url_for('static', filename='style.css')

if __name__ == '__main__':
    app.run(debug=True)


    # 首先我们导入了 Flask 类。这个类的实例将会成为我们的 WSGI 应用。
    # 接着我们创建了这个类的实例。第一个参数是应用模块或者包的名称。如果你使用一个 单一模块（就像本例），那么应当使用 __name__ ，因为名称会根据这个模块是按 应用方式使用还是作为一个模块导入而发生变化（可能是 '__main__' ，也可能是 实际导入的名称）。这个参数是必需的，这样 Flask 就可以知道在哪里找到模板和 静态文件等东西。更多内容详见 Flask 文档。
    # 然后我们使用 route() 装饰器来告诉 Flask 触发函数的 URL 。
    # 函数名称可用于生成相关联的 URL ，并返回需要在用户浏览器中显示的信息。
    # 最后，使用 run() 函数来运行本地服务器和我们的应用。 if __name__ == '__main__': 确保服务器只会在使用 Python 解释器运行代码的 情况下运行，而不会在作为模块导入时运行。
