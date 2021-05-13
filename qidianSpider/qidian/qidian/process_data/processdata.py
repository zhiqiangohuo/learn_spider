import json
import pandas as pd
import pickle
def readUserData():
    data = pd.read_csv('../data/readerinfo.csv', encoding='utf8')
    bookdict =[]
    readername = data['rname'].tolist()
    rreader = {}
    for i,user in enumerate(readername):
        # 按行合并所有等级的书单
        user_books = []
        for l in range(13):
            books = data['booklist{}'.format(l)][i]
            # print(books)
            user_books.extend(eval(books))
        # print(user,user_books)
        rreader[user]=user_books
    return rreader
def readeBookData():
    with open("../data/data.json", 'r') as f:
        book_id2tag = {}
        for line in f.readlines():
            line = line.split(', "intro"')[0]
            line = line+"}"
            data = json.loads(line)
            bookid = data['bookId']
            tag = data['tag']
            book_id2tag[bookid] = tag
        # print(book_id2tag)
    return book_id2tag

def createJsondata():
    # 创建统计用户读书类型的数据
    """
    {'悬疑': 0, '轻小说': 1, '短篇': 2, '历史': 3, '游戏': 4, '都市': 5, '奇幻': 6, '武侠': 7, '体育': 8, '军事': 9, '科幻': 10, '现实': 11, '玄幻': 12, '仙侠': 13}
    :param rreader:  读者  读到的书的信息 user:readbooks
    :param book_id2tag:  书id 到类型的 影射  id:tag
    :return:
    """
    rreader = readUserData()
    book_id2tag =readeBookData()
    none_see_book_id = []
    type = ['武侠', '历史', '短篇', '文学', '体育', '玄幻言情', '仙侠奇缘', '科幻空间', '悬疑推理', '现代言情', '古代言情', '都市', '游戏', '轻小说', '青春文学', '现实生活', '现实', '浪漫青春', '小说', '玄幻', '悬疑', '奇幻', '仙侠', '游戏竞技', '科幻', '军事']
    big_list = []
    for usr, red in rreader.items():
        user_info = {}
        user_reade_type = {i:0 for i in type}
        user_info['reader'] = usr
        for b in red:
            # b  书本id
            # print(book_id2tag[b])
            try:
                ty = book_id2tag[str(b)]
                user_reade_type[ty] += 1
            except Exception as e :
                # print("错误",e)
                pass
        # print(usr,user_reade_type)
        user_info['readbook'] =user_reade_type
        big_list.append(user_info)
    # print(big_list)
    f = open("reader_info.json",'w')
    json.dump(big_list,f,ensure_ascii=False , indent=2)


createJsondata()
#     for i, b in enumerate(book):
#         b = eval(b)
#         print(b, readername[i])
#         if b != []:
#             bookdict.extend(b)
#         break
#     break
