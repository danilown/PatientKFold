# PatientKFold

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/danilown/PatientKFold.svg)](https://github.com/danilown/PatientKFold/blob/main/LICENSE)
[![Python application](https://github.com/danilown/PatientKFold/actions/workflows/python-app.yml/badge.svg)](https://github.com/danilown/PatientKFold/actions/workflows/python-app.yml)

A simple K-Fold cross-validator with 'group' awareness. It will **ensure** that a group will not be on the `train_set` and `test_set` at the same time.

The best example is when working with medical data. When performing cross-validation, all data related to one patient muss be hold together in the same split and muss not leak to the other.

This class is inspired by scikit-learn's [K-Fold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html#sklearn.model_selection.KFold) and [GroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#sklearn.model_selection.GroupKFold) cross-validators, but (subjectively) easier to use and with better support for pandas `DataFrame` objects.

## Requirements

What libraries you need to install and how to install them.

``` python
numpy>=1.8.0
```

You can install them either manually or through the command:

``` bash
pip install -r requirements.txt
```

## Package Installation

If you want to use this class, you have two options:

A) Simply copy and paste it in your project;

B) Or install it through `pip` following the command bellow:

``` bash
pip install git+git://github.com/danilown/PatientKFold#egg=PatientKFold
```

Then, using it is as simples as:

```python
from PatientKFold import PatientKFold
```

> **Note 1**: As noted by [David Winterbottom](https://codeinthehole.com/tips/using-pip-and-requirementstxt-to-install-from-the-head-of-a-github-branch/), if you freeze the environment to export the dependencies, note that this will add the specific commit to your requirements, so it might be a good idea to delete the commit ID from it.
> ___
> **Note 2**: Due to the simplicity of this "package", this installation method was preferred over the more traditional [PyPI](https://pypi.org/).

## Usage

The following examples are going to show how you could use this class.

First example is splitting a list of patient ids into 5 Folds.

Example 1:

``` python
from PatientKFold import PatientKFold

patients = [1,2,3,4,5,6,7,8,9,10,11,12,13]
p = PatientKFold(patients, random_state=42)

for train_patients, test_patients in p:
    print(train_patients, test_patients)
    print('===')
```

Output:

``` python
# [10, 13, 6, 12, 9, 4, 5, 1, 2, 11] [8, 7, 3]
# ===
# [8, 7, 3, 12, 9, 4, 5, 1, 2, 11] [10, 13, 6]
# ===
# [8, 7, 3, 10, 13, 6, 5, 1, 2, 11] [12, 9, 4]
# ===
# [8, 7, 3, 10, 13, 6, 12, 9, 4, 2, 11] [5, 1]
# ===
# [8, 7, 3, 10, 13, 6, 12, 9, 4, 5, 1] [2, 11]
# ===
```

In the second example we split a pd.DataFrame into 5 Folds informing which column represents the patient id.

Example 2:

``` python
from PatientKFold import PatientKFold
import pandas as pd

patient_df = {
    'patient': [1,2,2,3,4,5,5,5],
    'other_columns': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
} 

patient_df = pd.DataFrame.from_dict(patient_df)

# patient_df =
#       patient | other_columns
# 0        1             a
# 1        2             b
# 2        2             c
# 3        3             d
# 4        4             e
# 5        5             f
# 6        5             g
# 7        5             h

p = PatientKFold(patient_df, col_patient_id='patient', random_state=42)

for n_fold, (train_patients, test_patients) in enumerate(p):
    print('===')
    print(f'FOLD: {n_fold}')
    print("train_patients:")
    print(train_patients)
    print("test_patients:")
    print(test_patients)
```

Output:

``` python
# FOLD: 0
# train_patients:
#       patient | other_columns
# 0        1             a
# 1        2             b
# 2        2             c
# 3        3             d
# 5        5             f
# 6        5             g
# 7        5             h
# test_patients:
#       patient | other_columns
# 4        4             e
# ===
#
# FOLD: 1
# train_patients:
#       patient | other_columns
# 0        1             a
# 3        3             d
# 4        4             e
# 5        5             f
# 6        5             g
# 7        5             h
# test_patients:
#       patient | other_columns
# 1        2             b
# 2        2             c
# ===
#
# FOLD: 2
# train_patients:
#       patient | other_columns
# 0        1             a
# 1        2             b
# 2        2             c
# 4        4             e
# 5        5             f
# 6        5             g
# 7        5             h
# test_patients:
#       patient | other_columns
# 3        3             d
# ===
#
# FOLD: 3
# train_patients:
#       patient | other_columns
# 0        1             a
# 1        2             b
# 2        2             c
# 3        3             d
# 4        4             e
# test_patients:
#       patient | other_columns
# 5        5             f
# 6        5             g
# 7        5             h
# ===
#
# FOLD: 4
# train_patients:
#       patient | other_columns
# 1        2             b
# 2        2             c
# 3        3             d
# 4        4             e
# 5        5             f
# 6        5             g
# 7        5             h
# test_patients:
#       patient | other_columns
# 0        1             a
```

## Testing

In order to test this class, just run:

```shell
python -m unittest
```

## Support

If you would like to see a new functionality, have a suggestion on how to make the documentation clearer or report a problem, you can open an [issue](https://github.com/danilown/PatientKFold/issues/new) here on Github or send me an e-mail danilownunes@gmail.com.
