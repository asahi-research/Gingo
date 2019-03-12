# Gingo
This is a repository for headline **G**enerat**i**o**n** of multi-len**g**ths **O**utpus in Japanese (Gingo). We conviniently call this task **Gingo**. In this repository, we provide preprocess scripts  of [JAMUL/JNC corpus](https://cl.asahi.com/api_data/jnc-jamul.html) and evaluation scripts for Japanese summarization in ROUGE metric.

## JAMUL

**JA**panese **MU**lti-**L**ength Headline Corpus (**JAMUL**) is a corpus containing 1,524 news articles and their length-sensitive headlines in 10, 13, and 26 characters long for digital media and their length-insensitive headlines for paper.
The articles and headlines were all published between September 2017 and March 2018.

`JAMUL.csv` is arranged in order of per line as below.

- article
- paper headline
- 26 characters headline
- 13 characters headline
- 10 characters headline 

You can get `JAMUL.csv` by sending e-mail to `media-lab-rndrpr[atmark]asahi.com` (please replace \[atmark\] to @).

### Requirements
- Python 3.4+
- mecab-python3
- pythonrouge

We have a requirements.txt file for installing them:
```
pip -r requirments.txt
```

### JAMUL preprocess script

- `filter_jamul.py`: filter script to create the same test set in our paper.

```
python jamul_filter.py --input_path ./JAMUL.csv --output_path ./testset.csv
```

## JNC Corpus
**J**apanese **N**ews **C**orpus (JNC) is a collection of 1,829,231 pairs of the three lead sentences of articles and their print headlines published from 2007 to 2016. We use this dataset to train our seq2seq model. You can can get JNC corpus for a fee ([more details](https://cl.asahi.com/api_data/jnc-jamul.html) ).

### JNC preprocess script

- `jnc_filter.py`: filter script to create the same training data in our paper.

```
python jnc_filter.py --input_path ./JNC-corpus.json --output_path ./output_dir
```


## ROUGE evaluation

- `eval_rouge.py`: ROUGE evaluation script 

We used the following options for `eval_rouge.py` in case of specifying 26 characters long.

```
python eval_rouge.py --reference /path/to/test_headlines_of_JAMUL --predict /path/to/generated_headlines --trim 26
```
