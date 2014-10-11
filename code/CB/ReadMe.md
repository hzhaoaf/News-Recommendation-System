##content-based推荐过程记录

###算法原理
	根据用户阅读历史，生成用户的兴趣图谱（使用keywords表示），然后基于关键词，到候选文章中选出和用户兴
	趣最相似的文章。整个过程可以分为三个部分：
	1. 对用户进行建模（生成user_profile），即生成用户的keywords;
	2. 对候选文章（candidate_items）进行分析和特征提取，通常也是提取文章的关键词，使用它们来表征文章；
	3. user_profile和candidate_items的相似度计算，返回TopN
	
###10.11版实现过程
这一版并未按照标准的content-based的做法来完成，而是为了快速实现，完成了最粗糙的一版。和标准做法的区别在2，3步，当前的做法是利用Xapian对所有的文章进行检索，然后利用信息检索的原理，使用user_keywords到系统里进行检索，返回relevant最高的文章合集，然后过滤掉用户的阅读历史，选出N篇文章，即为推荐结果。

具体如下：

	1.从训练集中获取用户阅读文章的标题，进行分词，去Stopwords，然后统计词频，返回TopN（=5）的词，即为用户的keywords.
	(代码：generate_user_profile.py)
	2.利用Xapian对所有的文章进行索引，目前一共索引4个fields：title, content, newsid, timestamp;当然title和content也
	都进行了分词和去停用词；(代码: index.py)
	3.使用1中生成的user_keywords，到2中建立的索引里进行search，索引方式为: title:k1 content:k1 title:k2 content:k2...
	返回结果数目为(用户阅读数+3)。然后将用户阅读的文章去掉，剩下的按照rank排序即为给用户的推荐结果。
	(代码：rec_news_by_keywords.py)
	
以上是主要的实现过程，代码库里还有一个preprocessing_data.py文件，这个是在一开始对训练集进行预处理，包括分词和去停用词，然后所有的操作都是基于预处理之后的训练集进行。

###可以改进的过程
	1.分词和去掉停用词之后，可以考虑将单字的情况去掉；
	2.阅读数较少的用户可以不给他推荐，比如低于10篇的用户就不推荐；
	3.在使用keyword上进行检索的时候，可以控制返回文章的时间区间，比如一定在用户最后一篇文章的前后1天；这个过程Xapian
	可以实现;
