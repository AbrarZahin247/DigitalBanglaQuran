# Search API Using Word2Vec Model from Gensim

The Search API utilizes the Word2Vec model from Gensim to enhance search functionality. The process involves the following steps:
---
1. **Keyword Expansion**  
   For a given keyword, the API generates a list of closely related words using the Word2Vec model. This expanded list of related terms helps capture a broader range of relevant words related to the original keyword.

2. **Sentence Matching**  
   Using the expanded list of keywords, the API searches through a collection of sentences. It identifies sentences that contain the highest number of matches with the retrieved keywords.

By expanding the search query with related terms and analyzing sentence content for keyword matches, the API aims to provide more accurate and relevant search results.
---

http://127.0.0.1:5000/search?max_words=30&threshold=0.25&keyword=%E0%A6%B6%E0%A6%BE%E0%A6%B8%E0%A7%8D%E0%A6%A4%E0%A6%BF

http://127.0.0.1:5000/search?max_words=30&threshold=0.25&keyword=%E0%A6%B6%E0%A6%BE%E0%A6%A8%E0%A7%8D%E0%A6%A4%E0%A6%BF