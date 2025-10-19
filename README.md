# Huffman Encoding
**TEAM KENSHI**
Shiva Semwal
Muhammed Shameel KV

DAA project on Huffman encoding.

---

## Contents

- Prerequisites
- Option A — Run the Jupyter Notebook (recommended for exploration & visualization)
- Option B — Run `main.py` (command-line usage)

---


## Prerequisites

- Python 3
- Optional: conda or virtualenv for isolating the environment


---

## Option A — Run the Jupyter Notebook (recommended)

1. Clone the repository (from the repo root):
```bash
git clone https://github.com/shemei666/huffmanencoding.git
cd huffmanencoding
```

2. (Optional) Create and activate a virtual environment:
3. Install dependencies:
```bash
pip install notebook numpy matplotlib networkx
```
4. Start Jupyter Notebook:

```bash
jupyter notebook
```

---

## Option B — Run `main.py` (command-line)

If you prefer running the implementation without the notebook:

1. First clone the repo.
```bash
git clone https://github.com/shemei666/huffmanencoding.git
cd huffmanencoding
```
2. Now use the command below to run the code
```bash
python main.py [-h] [--hcode HCODE] file output [code]

positional arguments:
  file           input file
  output         output file
  code           output code file

options:
  -h, --help     show this help message and exit
  --hcode HCODE  huffman code
```
### Example usages
Example usage to encode a text file `a.txt` and get output text `out.txt` and Huffman code `code.json`

```bash
python main.py a.txt out.txt code.json
```

Example usage to decode a text given a Huffman code `code.json` and encoded message `enc.txt` get output `out.txt` 

```bash
python main.py --hcode code.json enc.txt out.txt
```

Enjoy exploring the Huffman encoding project!

