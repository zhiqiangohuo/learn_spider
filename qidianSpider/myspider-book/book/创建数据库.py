sql = "CREATE TABLE `qidianspider`.`readerinfo`  (`rtype` text NULL,
`rurl` text NULL,
`rimg` text NULL,
`rtitle` text NULL,
`rauthor` text NULL,
`rintro` text NULL,
`rtag` text NULL,
`countword` text NULL,
`totalrecomment` text NULL,
`weekrecomment` text NULL,
`totalbook` text NULL,
`totalword` text NULL,
`totalday` text NULL

);"


keys =['rtype', 'rurl', 'rimg', 'rtitle', 'rauthor', 'rintro', 'rtag', 'countword', 'totalrecomment', 'weekrecomment', 'totalbook', 'totalword', 'totalday']
s = "`{}` text NULL,"
for key in keys:
    s = "`{}` text NULL,"
    s = s.format(key)
    print(s)