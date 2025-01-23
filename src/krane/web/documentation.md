# Introduction

Krane library is a lightweight bioinformatics python library that supports both the `CLI` and `GUI`. A step by step process on installation for either option is detailed below. The CLI works on any operating system that supports python package installation with `pip`, while the `GUI` works on most modern browsers.

To get started, follow the instructions outlined below.

## Using CLI:

### Prerequisites

Verify that the latest version of python is installed by opening the `terminal` or `cmd` and running the following command:

```bash
python
```

This will set the `terminal` or `cmd` to python mode if it is already installed. If otherwise, kindly follow documentation for your preferred OS.

### Installation

To start using **Gene Sequence** package, install using the command below:

```bash
pip install krane
```

This command will install the package. It is advised that separate environment is used for respective projects. Check online for best practices.

### Importing Package

Following successful installation, enter into a python environment and import package with the following command:

```python
from krane import Sequence
```

### Instantiating Object

Instantiate an gene sequence object to begin working with sequence strands using the command below:

```python
sequence = Sequence()
```

### Getting Sequence

To get started quickly, call the `get_sequence` method with the command:

```python
sequence.get_sequence()
```

An input dialog will appear, paste the *sequence strand* and hit `enter`, followed by the *sequence bio-type* and hit `enter` and finally the *sequence label* and hit `enter`

### Setting Sequence

Alternatively, call the `set_sequence` method with the command below:

```python
sequence.set_sequence(arg1, arg2, arg3)
```

and provide the following parameters:

* arg1: sequence strand
* arg2: sequence bio type
* arg3: sequence label

The order of parameters are important for accurate result and output. For example:

```python
sequence.set_sequence('ACGT', 'DNA', 'Label')
```

### Uploading File

Uploading of FASTA file is also supported. To begin, provide the path to file in drive to the `upload_sequence` method using the command below:

```python
sequence.upload_sequence('path-to-file.txt')
```

This could be a user generated file or a FASTA file from online platforms. For example:

```python
sequence.upload_sequence('../FASTA.txt')
```

### Generating Random Sequence

Random strand of either of **DNA** or **RNA** is also available. Call the `generate_sequence` method using the command below:

```python
sequence.generate_sequence(arg1, arg2)
```

and supply the following parameters:

* arg1: sequence length
* arg2: sequence bio type

For example:

```python
sequence.generate_sequence(40, 'RNA')
```

This is the fastest way to get up and running when working with CLI.

### Counting Base Frequency

To count nucleotides in a given sequence, call the `nucleotide_frequency` method with following command:

```python
sequence.nucleotide_frequency()
```

### DNA Transcription

For DNA transcription to RNA, call the `transcription` method using the command below:

```python
sequence.transcription()
```

This returns a strand with Thymine replaced with Uracil.

### Reverse Complement

To get the reverse complement of a particular sequence, call the `reverse_complement` method using the command below:

```python
sequence.reverse_complement()
```

This call will swap adenine with thymine and guanine with cytosine in the returned sequence strand.

### GC Content

The GC content of a sequence can be calculated by call the `gc_content` method using the command below:

```python
sequence.gc_content()
```

This call returns the GC Content in a sequence strand.

### Translate to Amino-acid

Translating bases or a sequence strand to aminoacid can be accomplished by calling the `translate_seq` method using the command below:

```python
sequence.translate_seq()
```

This returns the amino-acid version of the translated sequence strand.

### Getting Reading Frames

Grouping successive bases in a sequence of DNA that into codons for the amino acids encoded by the DNA is done using `gen_reading_frames` method. The command is shown below:

```python
sequence.gen_reading_frames()
```

This call returns a 6 reading frame of a sequence strand.

### Translating to Proteins

In order to translate a sequence strand into protein, call the `all_proteins_from_orfs` method using the command below:

```python
sequence.all_proteins_from_orfs()
```

It returns all the available proteins found in a given strand. This output could be further sorted to either get the longest or the shortest strand.

## Using GUI:

### Downloading Application

Click [Installer](https://dev.d2j6j4pgiubh78.amplifyapp.com/#installer) link for respective Operating System (OS) to get started. Then, navigate and clone the repository. The README.md document contains the step by step guide on how to build the desktop app for each OS.

Once successfully installed, double-click the application to launch the application.

### Getting Data

The GUI accepts data in three forms, namely:

* Manual input
* File upload
* Random sequence generation

To manually enter data, type in or paste sequence strand in the input `textarea`, select bio-type from the drop down, and input the sequence label in the label input. Click the `Submit` button to load your data. If successful, sequence summary will be displayed in the output `textarea`.

For file upload, click the `Select File` button. A dialog will appear, select a `.txt` FASTA file from drive and upload. On successful upload, the sequence summary will be displayed in the output `textarea`.

With random sequence generation, firstly select the checkbox under the `Submit` button. Then, select the sequence type from the drop down, and enter the desired length to be generated.

### Selecting Functions

A list of functions are available for manipulating and transforming sequence strands. These options are contained within the drop down menu above the output textarea. Some of them include:

* Sequence Summary
* Reverse Complement
* GC Content

The output is displayed in the output textarea.