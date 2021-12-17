# TMU Evaluation Corpus for Japanese Learners (TEC-JL)


## Data
- The TEC-JL is an evaluation dataset for Japanese grammatical error correction.
- You can get the dataset from this [URL](https://docs.google.com/forms/d/e/1FAIpQLSdBOoRuHaDuBuwuuYHrz6ILR6LQqIPw3AUL6XVEmvDFg8z_wQ/viewform).


## Scripts
- We provide scripts for preprocessing of the Lang-8 corpus.
- The TEC-JL is built from the [Lang-8 corpus](https://sites.google.com/site/naistlang8corpora/), so you need to remove documents with duplicate journal IDs.

### Requirements
- Python 3
- [langdetect](https://pypi.org/project/langdetect/)
- [python-Levenshtein](https://pypi.org/project/python-Levenshtein/)

### Usage
```bash
python make_pairs.py --input lang-8-20111007-2.0/lang-8-20111007-L1-v2.dat --output japanese.txt
python clean_data.py --input japanese.txt --output-src japanese.src --output-trg japanese.trg
```

## Citation
- The following paper should be cited in any publications that use our dataset.
```
@inproceedings{koyama-etal-2020-construction,
    title = "Construction of an Evaluation Corpus for Grammatical Error Correction for Learners of {J}apanese as a Second Language",
    author = "Koyama, Aomi  and  Kiyuna, Tomoshige  and  Kobayashi, Kenji  and  Arai, Mio  and  Komachi, Mamoru",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.26",
    pages = "204--211",
}
```
