# this script defines functions and sets variables.
# It uses information from the config file.
# Note: it always runs upon execution of snakemake

import csv
from collections import defaultdict
from glob import glob
from os.path import basename, splitext
import os
from sys import stderr

import yaml
import yamlordereddictloader

def readconfig (myfile):
    with open(myfile) as f:
        yaml_data = yaml.load(f, Loader=yamlordereddictloader.Loader)
        return dict(yaml_data)

def pconfig (myconfig):
    try:
        for key, value in myconfig.items():
            print ('\n> ',key,'\n',value)
    except AttributeError:
        print ('Invalid config. NOT dictionary')


config = readconfig('config.yml')

def create_contigs_file():
    ''' Prepare contigs of interest (bed)'''
    is_contigs = os.path.exists('metadata/contigs_of_interest.bed')
    path = list(config['refs'].values())[0] # 1st reference
    if not is_contigs:
        os.system(r'awk -f utils/contigs.bed.awk {}.fai > metadata/contigs_of_interest.bed'.format(path))


def create_fai():
    ''' Index reference (fai)'''
    files = glob('genomes_and_annotations/*/*.fa') + glob('genomes_and_annotations/*/*.fna')
    for reference in files:
        is_fai = os.path.exists('{}.fai'.format(reference))
        if not is_fai:
            os.system('samtools faidx {}'.format(reference))


def parsefai(fai):
    with open(fai) as fh:
        for l in fh:
            cname, clen, _, _, _ = l.split()
            clen = int(clen)
            yield cname, clen


def parsebed(bed):
    names = []
    with open(bed) as bd:
        for l in bd:
            name = l.split()[0]
            names.append(name)
    return names


def make_regions(rdict, window=1e6, base=1):
    window = int(window)
    ret = {}
    for refname, refpath in rdict.items():
        fai = refpath+".fai"
        windows = []
        curwin = []
        curwinlen = 0
        contigs_of_interest = parsebed('metadata/contigs_of_interest.bed')

        for cname, clen in parsefai(fai):
            if cname in contigs_of_interest:
                #print ('>> ', cname)
                for start in range(0, clen, window):
                    wlen = min(clen - start, window)
                    windows.append("{}:{:09d}-{:09d}".format(cname, start + base, start+wlen))
        ret[refname] = windows
    return ret


def make_chroms(rdict):
    ret = {}
    for refname, refpath in rdict.items():
        fai = refpath+".fai"
        ref = dict()
        scafs = []
        for cname, clen in parsefai(fai):
            if cname.lower().startswith("chr"):
                ref[cname] = [cname]
            else:
                scafs.append(cname)
        if scafs:
            ref["scaffolds"] = scafs
        ret[refname] = ref
    return ret


def _iter_metadata(s2rl_file):
    with open(s2rl_file) as fh:
        for samp in csv.DictReader(fh):
            yield samp


def make_runlib2samp(s2rl_file):
    rl2s = {}
    s2rl = defaultdict(list)

    for run in _iter_metadata(s2rl_file):
        if not run["library"] or run["library"].lower().startswith("blank"):
            # Skip blanks
            continue
        if run.get("Include", "Y") != "Y":
            # Remove non-sequenced ones
            continue
        rl = (run["run"], run["library"])
        samp = run["sample"]
        rl2s[rl] = samp
        s2rl[samp].append(rl)
    #print ('RUNLIB2SAMP: ',dict(rl2s))
    #print ('SAMP2RUNLIB: ',dict(s2rl))
    return dict(rl2s), dict(s2rl)


def stripext(path, exts=".txt"):
    if isinstance(exts, str):
        exts = [exts,]
    for ext in exts:
        if path.endswith(ext):
            path = path[:-len(ext)]
    return path

def make_samplesets(s2rl_file, setfile_glob):
    ssets = defaultdict(list)
    everything = set()
    for setfile in glob(setfile_glob):
        setname = stripext(basename(setfile), ".txt")
        with open(setfile) as fh:
            samples = [x.strip() for x in fh]
        ssets[setname] = samples
        everything.update(samples)
    ssets["all_samples"] = everything

    if not os.path.exists("output/samplelists"):
        os.makedirs("output/samplelists", exist_ok=True)
    with open("output/samplelists/GENERATED_FILES_DO_NOT_EDIT", "w") as fh:
        print("you're probably looking for", setfile_glob, file=fh)
    for setname, setsamps in ssets.items():
        fname = "output/samplelists/{}.txt".format(setname)
        try:
            with open(fname) as fh:
                currsamps = set([l.strip() for l in fh])
        except IOError:
            currsamps = set()
        if set(setsamps) != currsamps:
            with open(fname, "w") as fh:
                print("WARNING: updating sample sets, this will trigger reruns", setname, file=stderr)
                for s in sorted(setsamps):
                    print(s, file=fh)

    #print ('SAMPLESETS: ', {n: list(sorted(set(s))) for n, s in ssets.items()} )
    return {n: list(sorted(set(s))) for n, s in ssets.items()}
