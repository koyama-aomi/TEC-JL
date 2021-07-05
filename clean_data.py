from langdetect import detect
import Levenshtein
import unicodedata
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser(description="This program cleans data of Japanese sentence pairs.")
    parser.add_argument("-i", "--input", dest="input_path", type=str, metavar="<path to the input file>", required=True, help="Please set the path to the input file.")
    parser.add_argument("-os", "--output-src", dest="output_src_path", type=str, metavar="<path to the output file of the lerner sentences>", required=True, help="Please set the path to the output file of the learner sentences.")
    parser.add_argument("-ot", "--output-trg", dest="output_trg_path", type=str, metavar="<path to the output file of the corrected sentences>", required=True, help="Please set the path to the output file of the corrected sentences.")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    outputs = set()
    with open(args.input_path, "r", encoding="utf8") as input_file, open(args.output_src_path, "w") as src_file, open(args.output_trg_path, "w") as trg_file:
        for line in input_file:
            line = line.strip().split("\t")
            if len(line) != 2:
                continue
            src, trg = preprocess(line[0], line[1])
            if (src, trg) in outputs:
                continue
            if src and trg:
                outputs.add((src, trg))
                print(src, file=src_file)
                print(trg, file=trg_file)
def preprocess(src, trg):
    # if src and trg:
    #     src = normalize_sent(src)
    #     trg = normalize_sent(trg)

    if src and trg:
        trg = remove_some_comments(trg)

    if src and trg:
        src = remove_url(src)
        trg = remove_url(trg)

    if src and trg:
        trg = remove_long_sent(trg)

    if src and trg:
        src = remove_short_sent(src)
        trg = remove_short_sent(trg)

    if src and trg:
        src, trg = remove_no_edit_pair(src, trg)

    if src and trg:
        src, trg = remove_large_edit_distance_pair(src, trg)

    if src and trg:
        src = remove_non_japanese_sent(src)

    if src and trg:
        trg = remove_non_japanese_sent(trg)

    return src, trg


def normalize_sent(sent):
    sent = unicodedata.normalize("NFKC", sent)
    return sent


def remove_some_comments(sent):
    sent = re.sub(r"OK$", "", sent)
    sent = re.sub(r"ok$", "", sent)
    sent = re.sub(r"GOOD$", "", sent)
    sent = re.sub(r"good$", "", sent)
    sent = re.sub(r"OK!$", "", sent)
    sent = re.sub(r"ok!$", "", sent)
    sent = re.sub(r"GOOD!$", "", sent)
    sent = re.sub(r"good!$", "", sent)
    return sent


def remove_url(sent):
    sent = re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", sent)
    return sent


def remove_long_sent(sent, threshold=50):
    if len(sent) > threshold:
        return None
    else:
        return sent


def remove_short_sent(sent, threshold=2):
    if len(sent) <= threshold:
        return None
    else:
        return sent


def remove_no_edit_pair(src, trg):
    if src == trg:
        return None, None
    else:
        return src, trg


def remove_large_edit_distance_pair(src, trg, threshold=5):
    edit_distance = Levenshtein.distance(src, trg)
    if edit_distance > threshold:
        return None, None
    else:
        return src, trg


def remove_non_japanese_sent(sent):
    try:
        language = detect(sent)
    except:
        return None
    if language != "ja":
        return None
    else:
        return sent


if __name__ == "__main__":
    main()