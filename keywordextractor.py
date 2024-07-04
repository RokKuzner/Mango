import yake

def extract_keywords(text:str, keywords_to_extract:int = 15):
    #Extract the keywords
    extractor = yake.KeywordExtractor(top=keywords_to_extract, stopwords=None)
    keywords = extractor.extract_keywords(text)

    #Return the keywords in an array
    out = []
    for keyword, score in keywords:
        out.append(keyword)
    return out