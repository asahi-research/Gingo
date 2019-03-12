import argparse
from collections import defaultdict
import json
import MeCab
from pprint import pprint
from pythonrouge.pythonrouge import Pythonrouge
# mecab tagger - for stemming and filtering
mecab_tagger = MeCab.Tagger("-Ochasen")
# vocab defined here
vocab = defaultdict(lambda: len(vocab))


def mecab_filter(filename, trim=0):
    output = []
    with open(filename) as f:
        for line in f:
            sent = line.replace(" ", "")
            if trim > 0:
                sent = sent[:trim]
            mecab_parsed = [p.split()
                            for p in mecab_tagger.parse(sent).split('\n')]
            parsed_sent = [p[0] for p in mecab_parsed if len(p) > 1]
            # convert word to word_id to evaluate ROUGE
            output.append([vocab[w] for w in parsed_sent])
    return output


if __name__ == '__main__':
    # args
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", help="reference file")
    parser.add_argument("--predict", help="predict file")
    parser.add_argument("--output", default=None, help="output file path")
    parser.add_argument("--trim", type=int, default=0,
                        help="trimed the hyp by specified length")
    args = parser.parse_args()
    # read file and preprocess
    print("reading gold text {}".format(args.reference))
    gold = mecab_filter(args.reference, trim=0)
    gold = [[[g]] for g in gold]
    print("reading text {} then run python rouge".format(args.predict))
    predict = [[pred] for pred in mecab_filter(args.predict, trim=args.trim)]
    rouge_coinfig = {"summary_file_exist": False,
                     "summary": predict,
                     "reference": gold,
                     "n_gram": 2,
                     "ROUGE_SU4": False,
                     "ROUGE_L": True,
                     "recall_only": False,
                     "f_measure_only": False,
                     "stemming": False,
                     "stopwords": False,
                     "word_level": True,
                     "length_limit": False,
                     "use_cf": False,
                     "cf": 95,
                     "scoring_formula": 'average',
                     "resampling": True,
                     "samples": 1000,
                     "favor": True,
                     "p": 0.5}
    rouge = Pythonrouge(**rouge_coinfig)
    print('ROUGE score')
    pprint(rouge.calc_score())
