import pandas as pd               
import matplotlib.pyplot as plt  

plt.figure(figsize=(6,9))    # 顯示圖框架大小

labels = 'A','B','C','D','E','F' 
separeted = (0, 0, 0.3, 0, 0.3, 0)                  # 依據類別數量，分別設定要突出的區塊
size = [33,52,12,17,62,48]                        # 製作圓餅圖的數值來源

# plt.pie(size , labels = labels,autopct='%1.1f%%')
plt.pie(size,                           # 數值
        labels = labels,                # 標籤
        autopct = "%1.1f%%",            # 將數值百分比並留到小數點一位
        explode = separeted,            # 設定分隔的區塊位置
        pctdistance = 0.6,              # 數字距圓心的距離
        textprops = {"fontsize" : 12},  # 文字大小
        shadow=True)                    # 設定陰影

 
plt.axis('equal')                                          # 使圓餅圖比例相等
plt.title('Add and Delete', {"fontsize" : 18})  # 設定標題及其文字大小
plt.legend(bbox_to_anchor=(1.05, 1), loc = "best")                                   # 設定圖例及其位置為最佳
plt.tight_layout()
plt.show()
# plt.savefig("Pie chart of car accident.png",   # 儲存圖檔
#             bbox_inches='tight',               # 去除座標軸占用的空間
#             pad_inches=0.0)                    # 去除所有白邊
# plt.close()   