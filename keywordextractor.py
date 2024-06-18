import yake

def extract_keywords(text:str, keyword_to_word_ratio:float = 0.15):
    #Get the number of keywords to extract
    keywords_to_extract = int(len(text.split())*keyword_to_word_ratio)
    
    #Extract the keywords
    extractor = yake.KeywordExtractor(top=keywords_to_extract, stopwords=None)
    keywords = extractor.extract_keywords(text)

    #Return the keywords in an array
    out = []
    for keyword, score in keywords:
        out.append(keyword)
    return out