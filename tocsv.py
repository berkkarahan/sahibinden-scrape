from s_scrape.io import IO

import csv
import argparse

def load(fname):
    return IO.pickle_load(fname)

def write(outname):
    keys = list(l[0].keys())
    with open(outname, mode='w', newline='', encoding='utf-8') as f:
        fw = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fw.writerow(keys)

        for itm in l:
            try:
                print("--> Writing car: "+itm['Marka']+" with clsid: "+itm['clsid']+" to csv.")
                values = list(itm.values())
                fw.writerow(values)
            except TypeError:
                continue

parser = argparse.ArgumentParser()

parser.add_argument("--in", help="""Input filename of pickled details of listings.""", dest="input_file")
parser.add_argument("--ou", help="""Output csv file.""", dest="output_file")

args = parser.parse_args()

if __name__ == '__main__':
    l = load(args.input_file)
    write(args.output_file)
