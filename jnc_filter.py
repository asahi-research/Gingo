import argparse
from collections import Counter
import json
import os


def make_pair(path, idx, dataset):
    kiji, midashi = [], []
    for d in idx:
        x = dataset[d]
        kiji.append(''.join(x['kiji']))
        midashi.append(x['midashi'])
    with open('{}_kiji.txt'.format(path), 'w') as f:
        f.write('\n'.join(kiji))
    with open('{}_midashi.txt'.format(path), 'w') as f:
        f.write('\n'.join(midashi))


def construct_dataset(lines, data_path):
    kiji_counts = Counter([''.join(line['kiji']) for line in lines])
    midashi_counts = Counter([line['midashi'] for line in lines])
    exist_kiji, exist_mdiashi = set(), set()
    IDs = []
    dataset = {}
    # sort
    lines = sorted(lines, key=lambda k: k['kijiid'])
    for line in lines:
        kiji = ''.join(line['kiji'])
        midashi = line['midashi']
        kijiid = line['kijiid']
        # Use only kiji and midashi appeared only once and exclude txt including '='
        if kiji_counts[kiji] == 1 and midashi_counts[midashi] == 1 and '=' not in kiji:
            exist_kiji.add(kiji)
            exist_mdiashi.add(midashi)
            IDs.append(kijiid)
            dataset[kijiid] = line
    # data split
    train_size = int(len(IDs) * 0.98)
    holdout_size = int((len(IDs) - train_size) / 2)
    train = IDs[:train_size]
    valid = IDs[train_size:-holdout_size]
    test = IDs[-holdout_size:]
    print('total size: {}'.format(len(IDs)))
    print('size of train: {} valid: {} test: {}'.format(
        len(train), len(valid), len(test)))
    # write data
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    splited_data = [(os.path.join(data_path, 'train'), train),
                    (os.path.join(data_path, 'valid'), valid),
                    (os.path.join(data_path, 'test'), test)]
    for s in splited_data:
        output_path, idx = s
        make_pair(output_path, idx, dataset)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str,
                        default='./JNC-corpus.json',
                        help='path of JNC-corpus.json')
    parser.add_argument('--output_path', type=str,
                        default='./data_pair',
                        help='output path of kiji-midashi data pair of train/valid/test')
    args = parser.parse_args()
    with open(args.input_path) as f:
        jnc = [json.loads(line.strip()) for line in f.readlines()]
    print('json lines {}'.format(len(jnc)))
    construct_dataset(jnc, args.output_path)
