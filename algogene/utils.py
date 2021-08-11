# Base Nucleotides
NUCLEOTIDE_BASE = {
  "DNA": ["A", "T", "C", "G"],
  "RNA": ["A", "U", "C", "G"]
}

# Protein DNA CODONS
DNA_CODONS = {
  # 'M' - START, '_' - STOP
  "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
  "TGT": "C", "TGC": "C",
  "GAT": "D", "GAC": "D",
  "GAA": "E", "GAG": "E",
  "TTT": "F", "TTC": "F",
  "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
  "CAT": "H", "CAC": "H",
  "ATA": "I", "ATT": "I", "ATC": "I",
  "AAA": "K", "AAG": "K",
  "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
  "ATG": "M",
  "AAT": "N", "AAC": "N",
  "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
  "CAA": "Q", "CAG": "Q",
  "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
  "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
  "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
  "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
  "TGG": "W",
  "TAT": "Y", "TAC": "Y",
  "TAA": "_", "TAG": "_", "TGA": "_"
}

# Protein RNA CODONS
RNA_CODONS = {
  # 'M' - START, '_' - STOP
  "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
  "UGU": "C", "UGC": "C",
  "GAU": "D", "GAC": "D",
  "GAA": "E", "GAG": "E",
  "UUU": "F", "UUC": "F",
  "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
  "CAU": "H", "CAC": "H",
  "AUA": "I", "AUU": "I", "AUC": "I",
  "AAA": "K", "AAG": "K",
  "UUA": "L", "UUG": "L", "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
  "AUG": "M",
  "AAU": "N", "AAC": "N",
  "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
  "CAA": "Q", "CAG": "Q",
  "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
  "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S", "AGU": "S", "AGC": "S",
  "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
  "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
  "UGG": "W",
  "UAU": "Y", "UAC": "Y",
  "UAA": "_", "UAG": "_", "UGA": "_"
}

def colored(seq):
  bcolors = {
    'A': '\033[92m',
    'C': '\033[94m',
    'G': '\033[93m',
    'T': '\033[91m',
    'U': '\033[91m',
    'reset': '\033[0;0m'
  }
  tmpStr = ""
  for nuc in seq:
    if nuc in bcolors:
      tmpStr += bcolors[nuc] + nuc
    else:
      tmpStr += bcolors['reset'] + nuc
  return tmpStr + '\033[0;0m'


def readTextFile(filePath):
  with open(filePath, 'r') as f:
    return "".join([l.strip() for l in f.readlines()])


def writeTextFile(filePath, seq, mode='w'):
  with open(filePath, mode) as f:
    f.write(seq + '\n')


def read_FASTA(filePath):
  """Read file from local disk"""
  with open(filePath, 'r') as f:
    FASTAFile = [l.strip() for l in f.readlines()]

  FASTADict = {}
  FASTALabel = ""
  FASTASequence = ""
  FASTAType = ""

  for line in FASTAFile:
    if '>' in line:
      FASTALabel = line
      FASTADict[FASTALabel] = ""
    else:
      FASTASequence += line
      FASTADict[FASTALabel] += line
  FASTAType = 'DNA' if "T" in FASTASequence else 'RNA'

  return FASTASequence, FASTAType, FASTALabel
