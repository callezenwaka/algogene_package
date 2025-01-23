# import library
import os
import sys
import click
from ..core.sequence import Sequence, NUCLEOTIDE_BASE

def print_sequence_info(sequence_obj):
    """Helper function to format sequence information"""
    info = sequence_obj.get_sequence_info()
    click.echo(info)

@click.group()
def cli():
    """
    Krane - A DNA/RNA Sequence Analysis Tool

    This tool provides various functions for analyzing and manipulating DNA/RNA sequences.
    
    For detailed help on specific commands:\n
        krane analyze --help\n
        krane generate --help\n
        krane transcribe --help\n
        krane proteins --help\n
    
    Example usage:\n
        krane analyze ATCG --type DNA\n
        krane generate --length 20\n
        krane transcribe ATCG\n
    """
    pass

@cli.command('analyze')
@click.argument('sequence')
@click.option('--type', '-t', type=click.Choice(['DNA', 'RNA'], case_sensitive=False), 
              default='DNA', show_default=True,
              help='Type of sequence (DNA or RNA)')
@click.option('--label', '-l', default='No Label', show_default=True,
              help='Label for the sequence')
def analyze(sequence, type, label):
    """
    Analyze a DNA/RNA sequence and show its properties.

    SEQUENCE: The DNA/RNA sequence to analyze (e.g., ATCG). If SEQUENCE starts with "@",
    it will be treated as a file path, and the sequence will be read from the file.

    Examples:
        krane analyze ATCG
        krane analyze ATCG --type DNA --label "Test Sequence"
        krane analyze AUCG --type RNA
        krane analyze @sequence.fasta
    """
    if sequence.startswith('@'):
        file_path = sequence[1:]
        if not os.path.exists(file_path):
            click.echo(f"Error: File '{file_path}' not found", err=True)
            sys.exit(1)
        try:
            with open(file_path, 'r') as file:
                sequence = file.read().strip()
        except Exception as e:
            click.echo(f"Error reading file: {str(e)}", err=True)
            sys.exit(1)

    # Validate sequence based on type
    valid_nucleotides = {'DNA': 'ATCG', 'RNA': 'AUCG'}
    invalid_chars = set(sequence.upper()) - set(valid_nucleotides[type.upper()])

    if invalid_chars:
        click.echo(f"Error: Invalid characters in sequence: {', '.join(invalid_chars)}", err=True)
        sys.exit(1)

    try:
        seq = Sequence(sequence, type, label)
        print_sequence_info(seq)
        click.echo(f"\nNucleotide Frequency: {seq.nucleotide_frequency()}")
        click.echo(f"GC Content: {seq.gc_content()}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command('generate')
@click.option('--length', '-l', type=int, default=10, show_default=True,
              help='Length of sequence to generate')
@click.option('--type', '-t', type=click.Choice(['DNA', 'RNA'], case_sensitive=False),
              default='DNA', show_default=True,
              help='Type of sequence to generate')
def generate(length, type):
    """
    Generate a random DNA/RNA sequence.

    The sequence will contain random valid nucleotides based on the specified type.
    Valid nucleotides for DNA: A, T, C, G
    Valid nucleotides for RNA: A, U, C, G

    Examples:
        krane generate
        krane generate --length 20 --type DNA
        krane generate -l 15 -t RNA
    """
    if length <= 0:
        click.echo("Error: Length must be a positive number", err=True)
        return

    try:
        seq = Sequence()
        seq.generate_sequence(length, type)
        print_sequence_info(seq)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command('transcribe')
@click.argument('sequence')
def transcribe(sequence):
    """
    Transcribe a DNA sequence to RNA.

    SEQUENCE: The DNA sequence to transcribe (e.g., ATCG -> AUCG)

    Examples:
        krane transcribe ATCG
        krane transcribe ATGCCGT
    """
    try:
        seq = Sequence(sequence, "DNA")
        result = seq.transcription()
        click.echo(result)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command('proteins')
@click.argument('sequence')
@click.option('--type', '-t', type=click.Choice(['DNA', 'RNA'], case_sensitive=False),
              default='DNA', show_default=True,
              help='Type of input sequence')
@click.option('--sort', '-s', is_flag=True,
              help='Sort proteins by length (descending)')
def proteins(sequence, type, sort):
    """
    Find all possible proteins in a sequence.

    SEQUENCE: The DNA/RNA sequence to analyze for proteins

    The command will:
    1. Analyze all possible reading frames
    2. Find sequences between START (M) and STOP codons
    3. Return all possible protein sequences

    Examples:
        krane proteins ATGCCGTAA
        krane proteins AUGCCGUAA --type RNA
        krane proteins ATGCCGTAA --sort
    """
    try:
        seq = Sequence(sequence, type)
        proteins = seq.all_proteins_from_orfs(ordered=sort)
        if not proteins:
            click.echo("No proteins found in sequence")
            return
        
        click.echo(f"Found {len(proteins)} possible proteins:")
        for i, protein in enumerate(proteins, 1):
            click.echo(f"{i}. {protein} (length: {len(protein)})")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command('info')
def info():
    """
    Show information about valid nucleotides and sequence types.

    Displays:
    - Valid nucleotides for DNA and RNA
    - Basic information about the tool
    """
    click.echo("Krane - DNA/RNA Sequence Analysis Tool")
    click.echo("\nValid Nucleotides:")
    for seq_type, bases in NUCLEOTIDE_BASE.items():
        click.echo(f"{seq_type}: {', '.join(bases)}")
    click.echo("\nFor more information, visit: https://github.com/callezenwaka/krane")

if __name__ == '__main__':
    cli()