# In src/krane/web/routes/sequence.py
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ..schemas.sequence import HealthResponse
from ...core.sequence import Sequence
from ...core.models import SequenceCreate, SequenceResponse, ProteinResponse
from typing import List

router = APIRouter(tags=["sequence"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/analyze", response_model=SequenceResponse)
async def analyze_sequence(seq_input: SequenceCreate):
    try:
        seq = Sequence(
            sequence=seq_input.sequence,
            sequence_type=seq_input.sequence_type,
            label=seq_input.label
        )
        
        # Get nucleotide frequency removing the "[Base Frequency]: " prefix
        freq_str = seq.nucleotide_frequency()
        freq_dict = eval(freq_str.split(": ")[1])
        
        # Get GC content removing the "[GC CONTENT]: " prefix and the "%"
        gc_content = float(seq.gc_content().split(": ")[1].rstrip("%"))
        
        return SequenceResponse(
            sequence=seq.sequence,
            sequence_type=seq.sequence_type,
            label=seq.label,
            length=len(seq.sequence),
            gc_content=gc_content,
            nucleotide_frequency=freq_dict
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/proteins", response_model=ProteinResponse)
async def get_proteins(seq_input: SequenceCreate):
    try:
        seq = Sequence(
            sequence=seq_input.sequence,
            sequence_type=seq_input.sequence_type,
            label=seq_input.label
        )
        proteins = seq.all_proteins_from_orfs(ordered=True)
        return ProteinResponse(
            proteins=proteins,
            count=len(proteins)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transcribe")
async def transcribe_sequence(seq_input: SequenceCreate):
    try:
        seq = Sequence(
            sequence=seq_input.sequence,
            sequence_type=seq_input.sequence_type,
            label=seq_input.label
        )
        return {"transcribed_sequence": seq.transcription().split(": ")[1]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/documentation", response_class=HTMLResponse)
async def get_documentation(request: Request):
    return templates.TemplateResponse("documentation.html", {"request": request})

@router.get("/demo", response_class=HTMLResponse)
async def get_demo(request: Request):
    return templates.TemplateResponse("demo.html", {"request": request})