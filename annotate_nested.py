from flair.nn import Classifier
from flair.data import Sentence, Token
import json
import pathlib


TEST_DATA_PATH = ""  # iob formatted test file
MODEL_PATH = ""  # path to best-model.pt usually
TAGS_WITHOUT_NESTING = ["head"]  # any span classified with one of these tags will not be annotated again
OUT_PATH = "./nested_results/"


def read_test():
    """
    Read IOB Test data. The full document are marked by the filename headers with the character #.
    Mind you this might not work for all corpora.
    """
    metalist = []
    test_data = []
    with open(TEST_DATA_PATH, mode="r", encoding="utf8") as t:
        content = t.read()
    content = content.split("\n\n")
    for cont in content:
        cont = cont.split("\n")
        if not cont[0].startswith("#"):
            continue
        meta = cont[0]
        metalist.append(meta)
        cont = cont[1:]
        test_data.append(" ".join([t.split("\t")[0] for t in cont]))
    return test_data, metalist


def predict_recursive(sent, tagger, annotations, nest_heads=False, prev_sent_len=None, parent=None):
    if prev_sent_len == len(sent):
        # prevents endless loops
        return []

    sent = Sentence(sent, use_tokenizer=False)
    
    tagger.predict(sent)

    ents = sent.get_spans()

    for entity in ents:
        entity_dict = entity.to_dict()
        if nest_heads and entity.tag == "head" and parent is not None:
            if "head" in parent:
                parent["head"].append(entity_dict)
            else:
                parent["head"] = [entity_dict]
        else:
            annotations.append(entity_dict)
        
        if entity.tag in TAGS_WITHOUT_NESTING:
            continue
        # copy the tokens so they can be used for the next recursion
        tokens = []
        for token in entity.tokens:
            tokens.append(
                Token(
                    token.text,
                    whitespace_after=token.whitespace_after,
                    start_position=token.start_position
                )
            )
        predict_recursive(tokens, tagger, annotations, nest_heads=nest_heads, prev_sent_len=len(sent.tokens), parent=entity_dict)


if __name__ == "__main__":
    test_data, metalist = read_test()
    print(f"{len(test_data)} samples found.")
    print("Model loading.")
    tagger = Classifier.load(MODEL_PATH)
    all_annotations = []
    pathlib.Path(OUT_PATH).mkdir(parents=True, exist_ok=True) 
    with open(OUT_PATH, mode="w", encoding="utf8") as outf:
        for sent in test_data:
            annotations = []
            predict_recursive(sent, tagger, annotations, nest_heads=True)
            js = json.dumps(annotations)
            outf.write(js + "\n")
    print("Tagging finished.")