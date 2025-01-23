# tests/test_core.py - Test library functionality
import pytest
from krane.core.sequence import Sequence
from krane.core.models import SequenceType

def test_sequence_initialization():
    """Test basic sequence initialization"""
    seq = Sequence("ATCG", "DNA", "Test Label")
    assert seq.sequence == "ATCG"
    assert seq.sequence_type == "DNA"
    assert seq.label == "Test Label"

def test_invalid_sequence():
    """Test invalid sequence validation"""
    with pytest.raises(AssertionError):
        Sequence("ATCGX", "DNA")  # Invalid nucleotide X

def test_transcription():
    """Test DNA to RNA transcription"""
    seq = Sequence("ATCG", "DNA")
    result = seq.transcription()
    assert result == "[Transcription]: AUCG"

def test_nucleotide_frequency():
    """Test nucleotide frequency counting"""
    seq = Sequence("ATCGAA", "DNA")
    result = seq.nucleotide_frequency()
    freq = eval(result.split(": ")[1])  # Convert string repr to dict
    assert freq == {"A": 3, "T": 1, "C": 1, "G": 1}

def test_gc_content():
    """Test GC content calculation"""
    seq = Sequence("GCGC", "DNA")
    result = seq.gc_content()
    assert result == "[GC CONTENT]: 100%"

def test_reverse_complement():
    """Test reverse complement generation"""
    seq = Sequence("ATCG", "DNA")
    result = seq.reverse_complement()
    assert result == "[Reverse Complement]: CGAT"

def test_sequence_generation():
    """Test random sequence generation"""
    seq = Sequence()
    seq.generate_sequence(10, "DNA")
    assert len(seq.sequence) == 10
    assert all(base in "ATCG" for base in seq.sequence)

def test_translation():
    """Test sequence translation to amino acids"""
    seq = Sequence("ATGGCCTAT", "DNA")  # Codes for Met-Ala-Tyr
    result = seq.translate_seq()
    assert result == ["M", "A", "Y"]

def test_protein_finding():
    """Test finding proteins in sequence"""
    # ATG (start) GCC (Ala) TAA (stop)
    seq = Sequence("ATGGCCTAA", "DNA")
    proteins = seq.all_proteins_from_orfs()
    assert "MA" in proteins