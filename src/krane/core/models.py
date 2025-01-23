# src/krane/core/models.py
# from pydantic import BaseModel
# from typing import Optional, List

# class SequenceBase(BaseModel):
#     sequence: str
#     sequence_type: str = "DNA"
#     label: str = "No Label"

# class SequenceCreate(SequenceBase):
#     pass

# class SequenceResponse(SequenceBase):
#     length: int
#     gc_content: float
#     nucleotide_frequency: dict
    
#     class Config:
#         from_attributes = True

# class ProteinResponse(BaseModel):
#     proteins: List[str]
#     count: int

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class SequenceType(str, Enum):
    DNA = "DNA"
    RNA = "RNA"

class Sequence(BaseModel):
    """Core sequence model representing a DNA/RNA sequence."""
    sequence: str = Field(..., description="The sequence string")
    sequence_type: SequenceType = Field(..., description="Type of sequence (DNA or RNA)")
    label: str = Field(default="No Label", description="Label for the sequence")
    
    @field_validator('sequence')
    def validate_sequence(cls, v, values):
        """Validate sequence contains only valid nucleotides."""
        from ..core.sequence import NUCLEOTIDE_BASE
        sequence_type = values.get('sequence_type', 'DNA')
        valid_bases = set(NUCLEOTIDE_BASE[sequence_type])
        if not valid_bases.issuperset(v.upper()):
            raise ValueError(f"Invalid {sequence_type} sequence: contains invalid nucleotides")
        return v.upper()

class SequenceInfo(Sequence):
    """Model for sequence information response."""
    length: int = Field(..., description="Length of the sequence")

# Add these classes to your existing models.py file

class SequenceCreate(Sequence):
    """Model for sequence creation requests."""
    class Config:
        json_schema_extra = {
            "example": {
                "sequence": "ATCG",
                "sequence_type": "DNA",
                "label": "Example Sequence"
            }
        }

class SequenceResponse(SequenceInfo):
    """Model for sequence analysis response."""
    gc_content: float = Field(..., description="GC content percentage")
    nucleotide_frequency: Dict[str, int] = Field(..., description="Frequency of each nucleotide")

class NucleotideFrequency(BaseModel):
    """Model for nucleotide frequency response."""
    frequency: Dict[str, int] = Field(..., description="Frequency of each nucleotide")

class TranscriptionResult(BaseModel):
    """Model for transcription response."""
    transcribed_sequence: str = Field(..., description="Transcribed RNA sequence")

class GCContent(BaseModel):
    """Model for GC content response."""
    gc_content: float = Field(..., description="GC content percentage")

class ReverseComplement(BaseModel):
    """Model for reverse complement response."""
    reverse_complement: str = Field(..., description="Reverse complement sequence")

class AminoAcidSequence(BaseModel):
    """Model for amino acid sequence response."""
    amino_acids: List[str] = Field(..., description="List of amino acids")

class ProteinSequences(BaseModel):
    """Model for protein sequences response."""
    proteins: List[str] = Field(..., description="List of protein sequences")
    count: int = Field(..., description="Number of proteins found")

class ProteinResponse(ProteinSequences):
    """Model for protein analysis response."""

class ReadingFrames(BaseModel):
    """Model for reading frames response."""
    frames: List[List[str]] = Field(..., description="Six reading frames")