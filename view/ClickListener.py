# 设置点击事件
def setOnClickListener(view, func):
    view.clicked.connect(func)
