import pandas as pd
from matplotlib import pyplot as plt
import seaborn
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")

# 这一部分参考https://blog.csdn.net/h_hxx/article/details/90635650  直方图，散点图
# https://blog.csdn.net/weixin_39541558/article/details/79813936 热力图
class save_image():
    def __init__(self,excel_path):
        self.path = excel_path
        print(self.path)
        self.df = pd.read_excel(self.path)
    def save_hot_img(self):


        feature = ['poiId', 'avgScore', 'allCommentNum', 'avgPrice', 'hasAds']
        corr = self.df[feature].corr()
        cmap = seaborn.cubehelix_palette(start=5, rot=2, gamma=0.5, as_cmap=True)
        img = seaborn.heatmap(corr, vmin=-1, vmax=1, cmap=cmap, annot=True)
        plt.title("relatetion")
        fig = img.get_figure()
        fig.savefig('img/hot.png')
    def save_hist_img(self):
        relate = ['avgScore']
        score = self.df["avgScore"]
        print(score)
        plt.xlabel("avgScore")
        plt.ylabel('number')
        histimg = score.hist(figsize=(10, 5), bins=10)
        fig2 = histimg.get_figure()
        fig2.savefig('img/hist.png')
        # plt.show()
    def save_scatter_img(self):

        relate = ['allCommentNum', 'hasAds', 'avgPrice', 'avgScore']
        self.df.allCommentNum = self.df.allCommentNum / 10
        comment = self.df[relate]
        img = comment.plot.scatter(x='avgPrice', y='allCommentNum', s=comment['hasAds'], figsize=(10, 5))
        fig3 = img.get_figure()
        fig3.savefig('img/scatter.png')
    def save_all(self):
        self.save_hist_img()
        self.save_scatter_img()
        # self.save_hist_img()
        self.save_hot_img()
if __name__ == '__main__':
    s = save_image("./meituan.xls")
    s.save_all()