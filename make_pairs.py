import argparse
import json
import re


tecjl = [95652, 177778, 715422, 777469, 1065395, 664972, 627170, 597509, 136756, 427746,
953578, 983195, 1073665, 276920, 967431, 564422, 945421, 260887, 779547, 831645,
222711, 451442, 878669, 231348, 981621, 304944, 1035925, 425207, 889352, 913259,
228825, 63072, 431643, 899396, 965385, 124527, 757132, 1124968, 1070799, 298089,
383389, 724131, 716216, 1089491, 290840, 1044037, 873489, 308344, 207910, 66816,
157453, 941330, 984824, 1083067, 431419, 1111492, 114421, 50210, 156002, 804052,
379494, 648453, 1090244, 113166, 419427, 274190, 942221, 520924, 1068032, 948147,
89675, 604184, 806131, 344050, 1090763, 1031417, 568978, 438727, 121095, 1011743,
47733, 1109303, 140570, 123616, 490766, 863941, 400410, 1119717, 676673, 303119,
270650, 591056, 1039775, 745208, 711075, 1052873, 444706, 936281, 802941, 173586,
124581, 59635, 360410, 504768, 516054, 960459, 723381, 89917, 371210, 683934,
97822, 379286, 442117, 78882, 912027, 988396, 817387, 390945, 748278, 645871,
1060258, 27459, 820331, 351016, 172105, 920991, 144289, 898654, 428448, 1108849,
848794, 1060658, 518676, 933870, 1104123, 142372, 735249, 920268, 906241]

fluency_corpus = [555525, 585226, 622606, 953358, 602640, 652305, 188437, 912918, 378906, 571930, 
1041438, 845344, 841761, 351783, 167464, 358440, 1036333, 534573, 524845, 19506, 
1011255, 128056, 290874, 203837, 318014, 852544, 629313, 947778, 151104, 701511, 
687177, 939081, 625230, 270927, 953940, 947801, 993885, 139361, 973922, 806906, 
765547, 1056369, 889970, 575092, 1088119, 833655, 710267, 669823, 986752, 693380, 
836744, 744585, 140431, 759956, 759960, 311973, 47271, 535719, 259240, 130738, 
813234, 1031353, 307390, 943295, 143039, 205504, 435393, 1093322, 1087181, 179919, 
670419, 774868, 553689, 463079, 204522, 385772, 63214, 844528, 220914, 133879, 
139513, 1000185, 158459, 851194, 644351, 805120, 224000, 793858, 720134, 603399, 
561415, 475401, 769801, 155405, 246035, 767251, 270613, 131347, 513301, 218906, 
482074, 673564, 615709, 191268, 830757, 519973, 63271, 642855, 859960, 99647, 
90434, 162632, 176458, 76107, 1017163, 952653, 350539, 891220, 613730, 983906, 
222565, 203122, 703346, 811892, 529782, 1084279, 320887, 1028473, 763770, 503679, 
13186, 262534, 226702, 554895, 130449, 223122, 694163, 689042, 8088, 922011, 
969629, 817055, 337321, 273324, 484787, 689079, 620472, 966583, 1010108, 283070, 
36800, 981442, 613828, 67016, 521160, 939472, 279508, 1119701, 140767, 852448, 
521190, 162792, 680427, 210417, 281588, 136696, 865274, 930812, 862207]


def parse_args():
    parser = argparse.ArgumentParser(description="This program creates Japanese sentence pairs except ones used in the TEC-JL from the Lang-8 corpus.")
    parser.add_argument("-i", "--input", dest="input_path", metavar="<path to the input file>", required=True, help="Please set the path to the Lang-8 corpus (for example, ./lang-8-20111007-2.0/lang-8-20111007-L1-v2.dat).")
    parser.add_argument("-o", "--output", dest="output_path", metavar="<path to the output file>", required=True, help="Please set the path to the output file.")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    with open(args.input_path, "r", encoding="utf8") as input_file, open(args.output_path, "w") as output_file:
        for line in input_file:
            try:
                line = json.loads(line)
                journal_id = int(line[0])
                sentence_id = int(line[1])
                l2 = line[2]
                l1 = line[3]
                srcs = line[4] # ["learner_sentence1","learner_sentence2",...]
                trgs = line[5] # [["correction1_to_sentence1","correction2_to_sentence1",...], ["correction1_to_sentence2","correction2_to_sentence2",...], ...]
                if "Japanese" not in l2:
                    continue
                if journal_id in tecjl:
                    continue
                if journal_id in fluency_corpus:
                    continue
                outputs = make_pairs(srcs, trgs)
                for output in outputs:
                    print(output, file=output_file)
            except:
                pass


def make_pairs(srcs, trgs):
    outputs = []
    for i, src in enumerate(srcs):
        src = src.replace("\t", " ")
        src = remove_tags(src)
        if len(trgs[i]) == 0:
            output = src + "\t" + src
            outputs.append(output)
        else:
            for trg in trgs[i]:
                trg = trg.replace("\t", " ")
                trg = remove_tags(trg)
                output = src + "\t" + trg
                outputs.append(output)
    return outputs


def remove_tags(sent):
    sent = re.sub(r"\[f-red\]", r"", sent)
    sent = re.sub(r"\[f-blue\]", r"", sent)
    sent = re.sub(r"\[f-bold\]", r"", sent)
    sent = re.sub(r"\[赤\]", r"", sent)
    sent = re.sub(r"\[青\]", r"", sent)
    sent = re.sub(r"\[\/f-red\]", r"", sent)
    sent = re.sub(r"\[\/f-blue\]", r"", sent)
    sent = re.sub(r"\[\/f-bold\]", r"", sent)
    sent = re.sub(r"\[\/赤\]", r"", sent)
    sent = re.sub(r"\[\/青\]", r"", sent)
    sent = re.sub(r"\[sline\](.*)\[\/sline\]", r"", sent)
    return sent


if __name__ == "__main__":
    main()
