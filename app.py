from flask import Flask, request, jsonify
from gensim.models import Word2Vec
import json

app = Flask(__name__)

def return_find_sentence_and_index(word_list, data_dict, threshold=0.0, output_file="search_result.txt"):
    scored_sentences = []
    wordset = set(word_list)
    
    # Step 1: Calculate match counts and append to the list
    for key, value in data_dict.items():
        # Access the sentence and tokenized words
        sentence = value['sentence']
        received_word_list = value['tokenized_sentence']
        
        # Count matches with the word list
        match_count = sum(1 for word in received_word_list if word in wordset)
        scored_sentences.append((key, sentence, match_count))
    
    # Step 2: Find the maximum match count for normalization
    max_match_count = max(score for _, _, score in scored_sentences) if scored_sentences else 1  # Avoid division by zero
    
    # Step 3: Normalize the match counts
    normalized_scores = [(key, sentence, score / max_match_count) for key, sentence, score in scored_sentences]
    
    # Step 4: Filter sentences based on the threshold
    filtered_scores = [(key, sentence, score) for key, sentence, score in normalized_scores if score > threshold]
    
    # Step 5: Sort sentences by normalized score in descending order
    filtered_scores.sort(key=lambda x: x[2], reverse=True)
    return filtered_scores

def get_data_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as json_file:
        retrieved_string_dict = json.load(json_file)
    return retrieved_string_dict

def get_similar_wordlist(prompt,threshold = 0.8,top_n=None):
    final_word_list=[]
    model = Word2Vec.load("bangla_word2vec.model")
    if(top_n is None):
        similar_words = model.wv.most_similar(prompt, topn=10000)
        for word, similarity in similar_words:
            if similarity > threshold:
                final_word_list.append(word)
    else:
        similar_words = model.wv.most_similar(prompt, topn=top_n)
        for word, similarity in similar_words:
            final_word_list.append(word)
    return final_word_list

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/search', methods=['GET'])
def search():
    sura_names = [
        "সূরা আল ফাতিহা", "সূরা আল বাক্বারাহ", "সূরা আল ইমরান", "সূরা আন নিসা", "সূরা আল মায়েদাহ", 
        "সূরা আল আন-আম", "সূরা আল আ’রাফ", "সূরা আল-আনফাল", "সূরা আত তাওবাহ", "সূরা ইউনুস", 
        "সূরা হুদ", "সূরা ইউসূফ", "সূরা রা’দ", "সূরা ইব্রাহীম", "সূরা হিজর", 
        "সূরা নাহল", "সূরা বনী ইসরাঈল", "সূরা কাহফ", "সূরা মারইয়াম", "সূরা ত্বোয়া-হা", 
        "সূরা আম্বিয়া", "সূরা হাজ্জ্ব", "সূরা আল মু’মিনূন", "সূরা আন-নূর", "সূরা আল-ফুরকান", 
        "সূরা আশ-শো’আরা", "সূরা নমল", "সূরা আল কাসাস", "সূরা আল আনকাবুত", "সূরা আর-রূম", 
        "সূরা লোকমান", "সূরা সেজদাহ", "সূরা আল আহযাব", "সূরা সাবা", "সূরা ফাতির", 
        "সূরা ইয়াসীন", "সূরা আস-সাফফাত", "সূরা ছোয়াদ", "সূরা আল-যুমার", "সূরা আল-মু’মিন", 
        "সূরা হা-মীম সেজদাহ", "সূরা আশ-শুরা", "সূরা যুখরুফ", "সূরা আদ দোখান", "সূরা আল জাসিয়া", 
        "সূরা আল আহক্বাফ", "সূরা মুহাম্মদ", "সূরা আল ফাতহ", "সূরা আল হুজরাত", "সূরা ক্বাফ", 
        "সূরা আয-যারিয়াত", "সূরা আত্ব তূর", "সূরা আন-নাজম", "সূরা আল ক্বামার", "সূরা আর রহমান", 
        "সূরা আল ওয়াক্বিয়া", "সূরা আল হাদীদ", "সূরা আল মুজাদালাহ", "সূরা আল হাশর", "সূরা আল মুমতাহিনা", 
        "সূরা আছ-ছফ", "সূরা আল জুমুআহ", "সূরা মুনাফিকুন", "সূরা আত-তাগাবুন", "সূরা আত্ব-ত্বালাক্ব", 
        "সূরা আত-তাহরীম", "সূরা আল মুলক", "সূরা আল কলম", "সূরা আল হাক্বক্কাহ", "সূরা আল মা’আরিজ", 
        "সূরা নূহ", "সূরা আল জিন", "সূরা মুযযামমিল", "সূরা আল মুদ্দাসসির", "সূরা আল ক্বেয়ামাহ", 
        "সূরা আদ-দাহর", "সূরা আল মুরসালাত", "সূরা আন-নাবা", "সূরা আন-নযিআ’ত", "সূরা আবাসা", 
        "সূরা আত-তাকভীর", "সূরা আল ইনফিতার", "সূরা আত-তাতফীফ", "সূরা আল ইনশিক্বাক্ব", "সূরা আল বুরূজ", 
        "সূরা আত্ব-তারিক্ব", "সূরা আল আ’লা", "সূরা আল গাশিয়াহ", "সূরা আল ফজর", "সূরা আল বালাদ", 
        "সূরা আশ-শামস", "সূরা আল লায়ল", "সূরা আদ্ব-দ্বোহা", "সূরা আল ইনশিরাহ", "সূরা ত্বীন", 
        "সূরা আলাক", "সূরা কদর", "সূরা বাইয়্যিনাহ", "সূরা যিলযাল", "সূরা আদিয়াত", 
        "সূরা কারেয়া", "সূরা তাকাসূর", "সূরা আছর", "সূরা হুমাযাহ", "সূরা ফীল", 
        "সূরা কোরাইশ", "সূরা মাউন", "সূরা কাওসার", "সূরা কাফিরুন", "সূরা নছর", 
        "সূরা লাহাব", "সূরা এখলাছ", "সূরা ফালাক্ব", "সূরা নাস"
    ]
    # Get parameters from the request
    max_words = request.args.get('max_words', default=10, type=int)
    threshold = request.args.get('threshold', default=0.5, type=float)
    keyword = request.args.get('keyword', default="শান্তি", type=str)
    json_file_path="al_quran_sentences.json"
    data_dict=get_data_from_json(json_file_path)
    word_list=get_similar_wordlist(keyword,threshold,top_n=max_words)
    final_word_list=return_find_sentence_and_index(word_list,data_dict,threshold=0.66)
    master_word_list=[]
    for idx, sentence, score in final_word_list:
        idx_splited=idx.split('_')
        sura_index=int(idx_splited[0])-1
        sura_info=f"{sura_names[sura_index]}-{idx_splited[1]}"
        master_word_list.append({
            'sura_ayat':sura_info,
            'score':score,
            'ayat':sentence
        })
    # For demonstration purposes, we'll just return the parameters
    # In a real application, you would use these parameters to filter/search data
    return jsonify(master_word_list)

if __name__ == '__main__':
    app.run(debug=True)