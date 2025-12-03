import json
import re


STOPWORDS = {
    "a","an","the","is","am","are","was","were","be","been","being",
    "i","you","he","she","it","we","they","them","this","that","these","those",
    "and","or","but","if","because","as","until","while","of","at","by","for",
    "with","about","against","between","into","through","during","before","after",
    "above","below","to","from","up","down","in","out","on","off","over","under",
    "again","further","then","once","here","there","when","where","why","how",
    "all","any","both","each","few","more","most","other","some","such","no",
    "nor","not","only","own","same","so","than","too","very","can","will","just",
    "don","should","now","your","my","me","our","ours","their","theirs","his",
    "her","hers","its","what","which","who","whom","whose"
}


def extract_meaningful_words(text: str):
    text = text.lower()
    
    words = re.findall(r"[a-z]+", text)
    keywords = {w for w in words if w not in STOPWORDS}
    return sorted(list(keywords))



def generate_tags(input_path="knowledge_base.json", output_path="knowledge_base_tagged.json"):
    with open(input_path, "r") as f:
        data = json.load(f)

    for item in data:
        text = item.get("text", "")
        title = item.get("title", "")

       
        all_text = title + " " + text

        auto_tags = extract_meaningful_words(all_text)
        item["auto_tags"] = auto_tags     
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print("✔ auto_tags successfully generated and saved to:", output_path)



if __name__ == "__main__":
    generate_tags()
