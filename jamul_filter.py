import argparse
from collections import defaultdict
import MeCab
import re
repattern = re.compile("(「[^」]+」|（.+）)")
repattern_endsent = re.compile("([^。]+[。]?)")
mecab_tagger = MeCab.Tagger("-Owakati")


def tokenizer(sent):
    return mecab_tagger.parse(sent).strip().split()


def char_overlap(headline, article):
    overlap = len(set([w.lower() for w in tokenizer(headline) if len(w) > 1]) &
                  set([w.lower() for w in tokenizer(article) if len(w) > 1]))
    return overlap


def sentence_tokenizer(sents):
    quate_splitted = [s for s in repattern.split(sents)]
    output = []
    tmp = ""
    for i, block in enumerate(quate_splitted):
        if i % 2 == 0:
            splitted = repattern_endsent.findall(block)
            for j, s in enumerate(splitted):
                if j == len(splitted) - 1 and not s.endswith("。"):
                    tmp += s
                elif j == 0:
                    output.append(tmp + s)
                    tmp = ""
                else:
                    output.append(s)
        else:
            tmp += block
    if tmp:
        output.append(tmp)
    return output


def jamul_filter(path, length_limit=3):
    filtered_data = []
    with open(path) as f:
        lines = [line.strip().split(',')
                 for i, line in enumerate(f.readlines()) if i > 0]
    for line in lines:
        # idx[1] is shimen midashi which we don't use in this experiment
        art, char26, char13, char10 = line[0], line[2], line[3], line[4]
        if length_limit > 0:
            art = ''.join(sentence_tokenizer(art)[:length_limit])
        if not (len(char10) < 8 or len(char13) < 11 or len(char26) < 24 or '=' in art):
            match26 = char_overlap(char26, art)
            match13 = char_overlap(char13, art)
            match10 = char_overlap(char10, art)
            if not (match10 == 0 or match13 == 0 or match26 == 0):
                out_samples = '{},{},{},{}\n'.format(
                    art, char26, char13, char10)
                filtered_data.append(out_samples)
    return filtered_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str,
                        default='./JAMUL.csv',
                        help='path to JAMUL.csv')
    parser.add_argument('--output_path', type=str,
                        default='./testset.csv',
                        help='output path of filtered test set from JAMUL.csv')
    parser.add_argument('--length', type=int,
                        default=3,
                        help='sentence length limit for extracting JAMUL artcile. default=3 means LEAD-3')
    args = parser.parse_args()
    testdata = jamul_filter(args.input_path, length_limit=args.length)
    with open(args.output_path, 'w')as f:
        f.writelines(testdata)
