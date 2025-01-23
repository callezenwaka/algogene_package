# src/krane/web/schemas/sequence.py
from typing import Optional
from pydantic import BaseModel, Field
from ...core.models import (
    SequenceType, SequenceInfo, NucleotideFrequency,
    TranscriptionResult, GCContent, ReverseComplement,
    AminoAcidSequence, ProteinSequences, ReadingFrames
)

class HealthResponse(BaseModel):
    status: str = Field(..., description="API health status")

class SequenceCreate(BaseModel):
    """Schema for creating a new sequence."""
    sequence: str = Field(..., description="The sequence string")
    sequence_type: SequenceType = Field(..., description="Type of sequence (DNA or RNA)")
    label: str = Field(default="No Label", description="Label for the sequence")

class GenerateSequenceRequest(BaseModel):
    """Schema for generating a random sequence."""
    length: int = Field(..., gt=0, description="Length of sequence to generate")
    sequence_type: SequenceType = Field(..., description="Type of sequence to generate")

class FileUploadResponse(BaseModel):
    """Schema for file upload response."""
    filename: str
    sequence: str
    sequence_type: SequenceType
    label: str

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str

# Export response models
ResponseModels = {
    "info": SequenceInfo,
    "frequency": NucleotideFrequency,
    "transcription": TranscriptionResult,
    "gc_content": GCContent,
    "reverse_complement": ReverseComplement,
    "amino_acids": AminoAcidSequence,
    "proteins": ProteinSequences,
    "frames": ReadingFrames,
}