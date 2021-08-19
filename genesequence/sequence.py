from .utils import *
from collections import Counter
import random

class Sequence:
  """DNA sequence class. Defalt value: ATCG, DNA, No label"""

  def __init__(self, sequence="ATCG", sequence_type="DNA", label='No Label'):
    """Sequence initialization, validation."""
    self.sequence = sequence.upper()
    self.label = label.capitalize()
    self.sequence_type = sequence_type.upper()
    self.is_valid = self.__validate()
    assert self.is_valid, f"Provided data does not seem to be a correct {self.sequence_type} sequence"
  
  def __validate(self):
    """Check the sequence to make sure it is a valid DNA string"""
    return set(NUCLEOTIDE_BASE[self.sequence_type]).issuperset(self.sequence)
  
  def get_sequence_type(self):
    """Returns sequence type"""
    return self.sequence_type

  def get_sequence_info(self):
    """Returns 4 strings. Full sequence information"""
    return f"[Label]: {self.label}\n[Sequence]: {self.sequence}\n[Biotype]: {self.sequence_type}\n[Length]: {len(self.sequence)}"

  def generate_sequence(self, length=10, sequence_type="DNA"):
    """Generate a random DNA sequence, provided the length"""
    sequence = ''.join([random.choice(NUCLEOTIDE_BASE[sequence_type]) for x in range(length)])
    self.__init__(sequence, sequence_type, "Randomly generated sequence")
    
  def get_sequence(self):
    """Get a sequence strand, sequence type, and sequence length from user"""
    isReady = 'y'
    while isReady == 'y':
      sequence_strand = input("Enter sequence strand: ")
      sequence_type = input("Enter sequence type: ")
      sequence_label = input("Enter sequence label: ")
      try:
        self.__init__(sequence_strand, sequence_type, sequence_label)
        isReady = 'n'
      except:
        isReady = 'y'
      finally:
        isReady = input("\nWould you like to enter a new one? (y or n) ").lower()

  def set_sequence(self, sequence_strand, sequence_type, sequence_label):
    """Set sequence strand, sequence type, and sequence length from user input"""
    self.__init__(sequence_strand, sequence_type, sequence_label)
  
  def upload_sequence(self, path):
    """Upload sequence strand, sequence type, and sequence length from file input"""
    sequence_strand, sequence_type, sequence_label = read_FASTA(path)
    self.__init__(sequence_strand, sequence_type, sequence_label)

  def nucleotide_frequency(self):
    """Count nucleotides in a given sequence. Return a dictionary"""
    return f"[Base Frequency]: {dict(Counter(self.sequence))}"

  def transcription(self):
    """DNA -> RNA Transcription. Replacing Thymine with Uracil"""
    if self.sequence_type == "DNA":
      return f"[Transcription]: {self.sequence.replace('T', 'U')}"
    return "Not a DNA sequence"

  def reverse_complement(self):
    """
    Swapping adenine with thymine and guanine with cytosine.
    Reversing newly generated string
    """
    if self.sequence_type == "DNA":
      mapping = str.maketrans('ATCG', 'TAGC')
    else:
      mapping = str.maketrans('AUCG', 'UAGC')
    return f"[Reverse Complement]: {self.sequence.translate(mapping)[::-1]}"

  def gc_content(self):
    """GC Content in a DNA/RNA sequence"""
    return f"[GC CONTENT]: {round((self.sequence.count('C') + self.sequence.count('G')) / len(self.sequence) * 100)}%"

  def gc_content_subsec(self, k=20):
    """GC Content in a DNA/RNA sub-sequence length k. k=20 by default"""
    res = []
    for i in range(0, len(self.sequence) - k + 1, k):
      subseq = self.sequence[i:i + k]
      res.append(
        round((subseq.count('C') + subseq.count('G')) / len(subseq) * 100))
    return res

  def translate_seq(self, init_pos=0):
    """Translates a DNA sequence into an aminoacid sequence"""
    if self.sequence_type == "DNA":
      return [DNA_CODONS[self.sequence[pos:pos + 3]] for pos in range(init_pos, len(self.sequence) - 2, 3)]
    elif self.sequence_type == "RNA":
      return [RNA_CODONS[self.sequence[pos:pos + 3]] for pos in range(init_pos, len(self.sequence) - 2, 3)]

  def codon_usage(self, aminoacid):
    """Provides the frequency of each codon encoding a given aminoacid in a DNA sequence"""
    tmpList = []
    if self.sequence_type == "DNA":
      for i in range(0, len(self.sequence) - 2, 3):
        if DNA_CODONS[self.sequence[i:i + 3]] == aminoacid:
          tmpList.append(self.sequence[i:i + 3])

    elif self.sequence_type == "RNA":
      for i in range(0, len(self.sequence) - 2, 3):
        if RNA_CODONS[self.sequence[i:i + 3]] == aminoacid:
          tmpList.append(self.sequence[i:i + 3])

    freqDict = dict(Counter(tmpList))
    totalWight = sum(freqDict.values())
    for sequence in freqDict:
      freqDict[sequence] = round(freqDict[sequence] / totalWight, 2)
    return freqDict

  def gen_reading_frames(self):
    """Generate the six reading frames of a DNA sequence, including reverse complement"""
    frames = []
    frames.append(self.translate_seq(0))
    frames.append(self.translate_seq(1))
    frames.append(self.translate_seq(2))
    tmp_seq = Sequence(self.reverse_complement().split(" ")[-1], self.sequence_type)
    frames.append(tmp_seq.translate_seq(0))
    frames.append(tmp_seq.translate_seq(1))
    frames.append(tmp_seq.translate_seq(2))
    del tmp_seq
    return frames

  def proteins_from_rf(self, aa_seq):
    """Compute all possible proteins in an aminoacid sequence and return a list of possible proteins"""
    current_prot = []
    proteins = []
    for aa in aa_seq:
      if aa == "_":
        # STOP accumulating amino acids if _ - STOP was found
        if current_prot:
          for p in current_prot:
            proteins.append(p)
          current_prot = []
      else:
        # START accumulating amino acids if M - START was found
        if aa == "M":
          current_prot.append("")
        for i in range(len(current_prot)):
          current_prot[i] += aa
    return proteins

  def all_proteins_from_orfs(self, startReadPos=0, endReadPos=0, ordered=False):
    """Compute all possible proteins for all open reading frames"""
    """Protine Search DB: https://www.ncbi.nlm.nih.gov/nuccore/NM_001185097.2"""
    """API can be used to pull protein info"""
    if endReadPos > startReadPos:
      tmp_seq = Sequence(self.sequence[startReadPos: endReadPos], self.sequence_type)
      rfs = tmp_seq.gen_reading_frames()
    else:
      rfs = self.gen_reading_frames()

    res = []
    for rf in rfs:
      prots = self.proteins_from_rf(rf)
      for p in prots:
        res.append(p)

    if ordered:
      return sorted(res, key=len, reverse=True)
    return res