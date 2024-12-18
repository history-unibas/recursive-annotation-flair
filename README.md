# recursive-annotation-flair
This script will annotate a collection of sentences recursively and will generate nested annotations as output. The framework underlying it is [flairNLP](https://flairnlp.github.io/), so you can use any model Flair can use. 

For some more background, please see the associated presentation/paper in the Citation-section.

## Requirements
The script was tested with Python Version 3.11, but older and newer versions should likely also work as long as they are compatible with a working Flair version.

Install Flair if not already present:
```
pip3 install flair
```
The script was tested to work with Flair Version 0.13.1, but should likely also work with older and newer versions.

## How to use
Simply clone the repository where you like it. At the top of the script, insert the path to your input data and the model you want to use.

### Input Data
Currently the script requires a file in IOB-format (also known as column- or conll-format). Each sentence you'd like to annotate must be preceded by a line starting with a `#` (comment line).

If you know a bit of Python, it should be very easy to modify the main clause to simply take a text file and annotate it line-by-line. If you do so, we appreciate if you create a pull request with your version (and maybe we'll do it ourselves at some point).

### Model
You can either write a path to a model in your local files, or to Huggingface, just as you can do in Flair itself.

Mind you recursive annotation works best with specialized models. See our associated presentation/paper.

Openly available, specialized models:
| model | language | domain |
| :---: | :---: | :---: |
| [dh-unibe/hgb-ner-v1](https://huggingface.co/dh-unibe/hgb-ner-v1) | Historical German | 14th-17th c. property and rent transactions from the city of Basel

### Output
The data will be output in a `jsonl`-file with a json-encoded string on each line.
Head elements are automatically added to their parent spans, but you can turn this off by changing the `nest_heads`-parameter in the main-clause to `False`.

## Citation
If you use this script for any published works, please cite this work:

Prada Ziegler, I. (2024, May 30). What's in an entity? Exploring Nested Named Entity Recognition in the Historical Land Register of Basel (1400-1700). DH Benelux 2024, Leuven, Belgium. Zenodo. https://doi.org/10.5281/zenodo.11394453
