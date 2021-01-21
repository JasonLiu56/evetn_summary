# 主要用于发布文章
from pytypecho import Typecho, Post, Comment
from settings import blog_url, blog_username, blog_password


# 发布文章工具类
class TypechoUtils():
    def __init__(self, url=blog_url, username=blog_username, password=blog_password):
        self.client = Typecho(url, username, password)

    def add_article(self, title, sentences):
        if len(sentences) > 0:
            self.post = Post(title=title, description="\n".join(sentences))
            self.client.new_post(self.post, publish=True)


if __name__ == '__main__':
    utils = TypechoUtils()
    utils.add_article(title="标题", sentences=["内容1", "内容2"])