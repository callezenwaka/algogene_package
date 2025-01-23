# src/krane/core/__init__.py
from .sequence import Sequence
from .models import (
    SequenceType,
    SequenceInfo,
    NucleotideFrequency,
    TranscriptionResult,
    GCContent,
    ReverseComplement,
    AminoAcidSequence,
    ProteinSequences,
    ReadingFrames,
    SequenceCreate,  # Add new model
    SequenceResponse,  # Add new model
    ProteinResponse  # Add new model
)

try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("krane")
    except PackageNotFoundError:
        __version__ = "unknown"
except ImportError:
    __version__ = "unknown"

__all__ = [
    'Sequence',
    'SequenceType',
    'SequenceInfo',
    'NucleotideFrequency',
    'TranscriptionResult',
    'GCContent',
    'ReverseComplement',
    'AminoAcidSequence',
    'ProteinSequences',
    'ReadingFrames',
    'SequenceCreate',  # Add new model
    'SequenceResponse',  # Add new model
    'ProteinResponse'  # Add new model
]