import random
import numpy as np

try:
    import pandas as pd
except ImportError:
    # pandas is not installed in the system, the class probably will not be 
    # used with it
    pd = None

class PatientKFold:

    def __init__(self, 
        patients,
        n_folds=5,
        shuffle=True,
        col_patient_id=None,
        random_state=None
    ):
        """Splits a list of patients or a pd.DataFrame into n_folds to perform
           cross-validation

        Parameters:

            patients: list or pd.DataFrame
                Data to be split. If pd.DataFrame, col_patient_id 
                must be provided.

            n_folds: int, default=5
                Number of folds. Must be at least 2.

            shuffle: bool, default=True
                If True, the data will be shuffled before splitting into batches.

            col_patient_id: str, default=None
                if patients is a pd.DataFrame, it indicates which column holds the 
                information about the patients (patient_id).

            random_state: int, default=None
                Random state used with shuffle=True

        Raises:
            ValueError: When the amount of patients or the amount of folds is incorrect. 
            TypeError: When passing something that is not a list of a pd.DataFrame
                       as patients.
        """
        
        if len(patients) <= 1:
            raise ValueError(
                "The amount of patients has to be at least 2"
                " got len(patients)={0}.".format(len(patients))
            )

        if n_folds <= 1:
            raise ValueError(
                "Cross-validation requires at least one"
                " train/test split by setting n_folds=2 or more,"
                " got n_folds={0}.".format(n_folds)
            )

        self.n_folds = n_folds

        if random_state:
            random.seed(random_state)

        self.df_patients = None
        self.col_patient_id = col_patient_id

        if not isinstance(patients, list):
            if pd and isinstance(patients, pd.DataFrame):
                self.df_patients = patients
                patients = self.df_patients[self.col_patient_id]
            else:
                # class not defined for this type of object
                raise TypeError

        # certifying that the patients are unique
        patients = list(set(patients))

        if shuffle:
            # shuffling because are going to use a 'slidding window' to 
            # perform the folds
            random.shuffle(patients)

        # print('shuffle: ', patients)

        self.patients = patients

        self.__current_fold = 0 

        # getting the fold sizes for each fold
        # and distributing the 'extra' samples
        # using the sklearn strategy: 
        # https://github.com/scikit-learn/scikit-learn/blob/0d378913b/sklearn/model_selection/_split.py#L365
        fold_sizes = np.full(
                            self.n_folds, 
                            len(self.patients) // self.n_folds, dtype=int
                          )
        fold_sizes[: len(self.patients)  % self.n_folds] += 1
        
        self.fold_ind = [None] * self.n_folds
        current_idx = 0
        for fold, fold_size in enumerate(fold_sizes):
            start, stop = current_idx, current_idx + fold_size
            current_idx = stop
            self.fold_ind[fold] = (start, stop)

        # print('self.fold_ind: ', self.fold_ind)

    def __iter__(self):
        self.__current_fold = 0
        return self

    def __next__(self):
        if self.__current_fold < self.n_folds:

            train_patients, test_patients = self.__getitem__(self.__current_fold)

            self.__current_fold += 1

            return train_patients, test_patients

        else:
            raise StopIteration
    
    def __getitem__(self, fold):
        if fold < 0 or fold >= self.n_folds:
            raise IndexError

        start, stop = self.fold_ind[fold] 

        test_patients = self.patients[start:stop]

        if fold == 0:
            train_patients = self.patients[stop:]

        else:
            train_patients = self.patients[0:start] + \
                             self.patients[stop:]

        #print('test_patients: ', test_patients)
        #print('train_patients: ', train_patients)

        # if it is a pd.Dataframe
        if self.df_patients is not None:
            train_patients = self.df_patients[
                self.df_patients[self.col_patient_id].isin(train_patients)
            ]

            test_patients = self.df_patients[
                self.df_patients[self.col_patient_id].isin(test_patients)
            ]

        return train_patients, test_patients