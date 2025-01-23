# 
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from ...core.sequence import Sequence as SequenceAnalyzer
from ..schemas.sequence import FileUploadResponse, ErrorResponse
import os
from typing import List

router = APIRouter(prefix="/utils", tags=["utilities"])

@router.post(
    "/upload",
    response_model=FileUploadResponse,
    responses={400: {"model": ErrorResponse}}
)
async def upload_sequence_file(file: UploadFile = File(...)):
    """Upload a FASTA file for sequence analysis."""
    try:
        # Read file content
        content = await file.read()
        text = content.decode()
        
        # Parse FASTA content
        lines = text.split('\n')
        sequence = ""
        label = "No Label"
        
        for line in lines:
            line = line.strip()
            if line.startswith('>'):
                label = line
            elif line:
                sequence += line
        
        # Determine sequence type
        sequence_type = "DNA" if "T" in sequence else "RNA"
        
        # Validate sequence
        analyzer = SequenceAnalyzer(sequence, sequence_type, label)
        
        return FileUploadResponse(
            filename=file.filename,
            sequence=analyzer.sequence,
            sequence_type=sequence_type,
            label=label
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/valid-bases/{sequence_type}")
async def get_valid_bases(sequence_type: str):
    """Get valid nucleotide bases for a sequence type."""
    from ...core.sequence import NUCLEOTIDE_BASE
    
    if sequence_type.upper() not in NUCLEOTIDE_BASE:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sequence type. Must be one of {list(NUCLEOTIDE_BASE.keys())}"
        )
    
    return {"bases": NUCLEOTIDE_BASE[sequence_type.upper()]}

@router.get("/codons/{sequence_type}")
async def get_codons(sequence_type: str):
    """Get codon table for a sequence type."""
    from ...core.sequence import DNA_CODONS, RNA_CODONS
    
    if sequence_type.upper() == "DNA":
        return {"codons": DNA_CODONS}
    elif sequence_type.upper() == "RNA":
        return {"codons": RNA_CODONS}
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid sequence type. Must be either DNA or RNA"
        )

@router.get("/amino-acids")
async def get_amino_acids():
    """Get list of all possible amino acids."""
    from ...core.sequence import DNA_CODONS
    
    amino_acids = set(DNA_CODONS.values())
    amino_acids.discard('_')  # Remove stop codon
    return {"amino_acids": sorted(list(amino_acids))}