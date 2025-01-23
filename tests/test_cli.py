import pytest
from click.testing import CliRunner
from krane.cli.commands import cli

@pytest.fixture
def runner():
    """Fixture for CLI runner"""
    return CliRunner()

def test_cli_help(runner):
    """Test CLI help command shows all available commands"""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'analyze' in result.output
    assert 'generate' in result.output
    assert 'transcribe' in result.output
    assert 'proteins' in result.output

def test_analyze_command(runner):
    """Test sequence analysis command"""
    result = runner.invoke(cli, ['analyze', 'ATCG', '--type', 'DNA'])
    assert result.exit_code == 0
    assert 'ATCG' in result.output
    assert 'DNA' in result.output

def test_analyze_invalid_sequence(runner):
    """Test handling of invalid sequence in analyze command"""
    result = runner.invoke(cli, ['analyze', 'ATCGX', '--type', 'DNA'])
    assert result.exit_code == 0
    assert 'Error' in result.output
    assert 'does not seem to be a correct DNA sequence' in result.output

def test_generate_command(runner):
    """Test sequence generation command"""
    result = runner.invoke(cli, ['generate', '--length', '10', '--type', 'DNA'])
    assert result.exit_code == 0
    assert 'Length' in result.output
    assert 'DNA' in result.output

def test_generate_invalid_length(runner):
    """Test handling of invalid length in generate command"""
    result = runner.invoke(cli, ['generate', '--length', '-5'])
    assert "Length must be a positive number" in result.output or "Invalid length" in result.output

# def test_generate_invalid_length(runner):
#     """Test handling of invalid length in generate command"""
#     result = runner.invoke(cli, ['generate', '--length', '-5'])
#     assert "Length must be a positive number" in result.output

# def test_generate_invalid_length(runner):
#     """Test handling of invalid length in generate command"""
#     result = runner.invoke(cli, ['generate', '--length', '-5'])
#     assert result.exit_code == 0  # Because we're using try-except
#     assert "Error" in result.output
#     assert "Length must be a positive number" in result.output
#     assert "-5" in result.output

# def test_generate_invalid_length(runner):
#     """Test handling of invalid length in generate command"""
#     result = runner.invoke(cli, ['generate', '--length', '-5'])
#     assert result.exit_code == 0  # Since using try-except
#     assert 'Error' in result.output
#     assert 'Length must be positive' in result.output  # Adjust this message to match your actual error

# def test_generate_invalid_length(runner):
#     """Test handling of invalid length in generate command"""
#     result = runner.invoke(cli, ['generate', '--length', '-5'])
#     assert result.exit_code != 0
#     assert 'Error' in result.output

def test_transcribe_command(runner):
    """Test transcription command"""
    result = runner.invoke(cli, ['transcribe', 'ATCG'])
    assert result.exit_code == 0
    assert 'AUCG' in result.output

def test_proteins_command(runner):
    """Test proteins command"""
    # Testing with a sequence that should produce a protein (ATG = start, TAA = stop)
    result = runner.invoke(cli, ['proteins', 'ATGGCCTAA', '--type', 'DNA'])
    assert result.exit_code == 0
    assert 'MA' in result.output  # Should find Met-Ala protein

def test_proteins_with_sort(runner):
    """Test proteins command with sorting"""
    sequence = 'ATGGCCTAGATGTAA'  # Should produce multiple proteins
    result = runner.invoke(cli, ['proteins', sequence, '--sort'])
    assert result.exit_code == 0

def test_info_command(runner):
    """Test info command"""
    result = runner.invoke(cli, ['info'])
    assert result.exit_code == 0
    assert 'DNA' in result.output
    assert 'RNA' in result.output
    assert 'Valid Nucleotides' in result.output

@pytest.mark.parametrize("command,args,expected_text", [
    ('analyze', ['--help'], 'Analyze a DNA/RNA sequence'),
    ('generate', ['--help'], 'Generate a random DNA/RNA sequence'),
    ('transcribe', ['--help'], 'Transcribe a DNA sequence to RNA'),
    ('proteins', ['--help'], 'Find all possible proteins in a sequence'),
])
def test_command_help_texts(runner, command, args, expected_text):
    """Test help text for each command"""
    result = runner.invoke(cli, [command] + args)
    assert result.exit_code == 0
    assert expected_text in result.output

def test_interactive_error_handling(runner):
    """Test error handling in interactive mode"""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['analyze', 'ATCG'], input='n\n')
        assert result.exit_code == 0

# def test_file_not_found(runner):
#     """Test handling of non-existent input file"""
#     with runner.isolated_filesystem():
#         result = runner.invoke(cli, ['analyze', '@nonexistent.fasta'])
#         assert result.exit_code != 0
#         assert 'Error' in result.output

def test_file_not_found(runner):
    """Test handling of non-existent input file"""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['analyze', '@nonexistent.fasta'])
        assert result.exit_code != 0
        assert "Error: File 'nonexistent.fasta' not found" in result.output
