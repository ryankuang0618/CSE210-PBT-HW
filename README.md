# README

## Overview

This workspace contains several Python scripts located in the `executable_files` directory. Each script loads and executes a corresponding encoded Python module from the `__encoded_files__` directory.


## Prerequisites

- Python 3.11.8
- It is recommended to install this Python version with conda. To create a new Conda environment with Python 3.11.8:  
  ```sh
      conda create --n py3118_env python=3.11.8
- Ensure that the `__encoded_files__` directory contains the encoded `.pyc` files: `q1.encoded.pyc`, `q2.encoded.pyc`, `q3.encoded.pyc`, `q4.encoded.pyc`, and `q5.encoded.pyc`.

## Running the Scripts

### `executable_files/run_q1.py`

  ```sh
  cd executable_files
  python run_q1.py
  ```

## Running the Testing Scripts

```sh
conda activate py3118_env
pip install python-dateutil
pytest test_transpose.py
pytest test_parse_date.py
pytest test_binary_search.py
pytest test_lru_cache.py
pytest test_merge_sort.py
```