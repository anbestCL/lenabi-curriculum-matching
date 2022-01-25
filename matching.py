import json
import treetaggerwrapper
import nltk 
from nltk.corpus import stopwords

nltk.download('stopwords')
STOPWORDS = stopwords.words('german')
TAGGER = treetaggerwrapper.TreeTagger(TAGLANG='de', TAGDIR='/Users/anbest/Downloads/tree-tagger-MacOSX-3.2.3/')

def clean(heading_list):
    # removing symbols
    words = [heading.split("(ca.")[0] for heading in heading_list]
    words = " ".join(words).split()
    
    # removing stopwords
    words = [word for word in words if word not in STOPWORDS]

    # remove duplicates
    words = list(set(words))

    # Funktionen -> Funktion
    words = lemmatize(words)
    return words

def lemmatize(word_list, tagger = TAGGER):
    tags = tagger.tag_text(" ".join(word_list))
    tags2 = treetaggerwrapper.make_tags(tags)
    return [Tag.lemma for Tag in tags2]

def get_headings(cur, level="top"):
    if level == "top":
        queries = clean(cur.keys())
    elif level == "subtopic":
        headings = []
        for topic, subtopics in cur.items():
            headings.append(topic)
            for subtopic in subtopics:
                headings.append(subtopic["name"])
        queries = clean(headings)
#        queries = ",".join(headings).split()
    return queries

def find_matches(cur, query):
    matches = []
    for level in cur["children"]:
        for topic in level["children"]:
            # partial match
            if query in topic["name"]:
                matches.append("&".join([level["name"],topic["name"]]))

    return matches

# Main routine

file_bav = open('bayern-mathematik-9.json')
cur_bav = json.load(file_bav)

file_sax = open("output/sachsen-mathematik.json")
cur_sax = json.load(file_sax)

queries = get_headings(cur_bav, level="subtopic")
matches = {}
for query in queries:
    matches[query] = find_matches(cur_sax, query)

for keyword in matches:
    print(keyword)
    print(matches[keyword])
    print("\n")



file_bav.close()
file_sax.close()

