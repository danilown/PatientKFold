import unittest

from PatientKFold.PatientKFold import PatientKFold
import pandas as pd

class TestPatientKFold(unittest.TestCase):
    def test_simple_split(self):
        """
        Split of a simple list of integers into 5 folds
        iterate over them and try to select them by indexing
        """
        test_list_patients = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        results = [
            ([10, 13, 6, 12, 9, 4, 5, 1, 2, 11], [8, 7, 3]),
            ([8, 7, 3, 12, 9, 4, 5, 1, 2, 11], [10, 13, 6]),
            ([8, 7, 3, 10, 13, 6, 5, 1, 2, 11], [12, 9, 4]),
            ([8, 7, 3, 10, 13, 6, 12, 9, 4, 2, 11], [5, 1]),
            ([8, 7, 3, 10, 13, 6, 12, 9, 4, 5, 1], [2, 11]),
        ]

        p = PatientKFold(test_list_patients, random_state=42)

        # test looping
        for fold, (train_patients, test_patients) in enumerate(p):
            self.assertEqual(train_patients, 
                             results[fold][0], 'Fail while looping')
            self.assertEqual(test_patients, 
                             results[fold][1], 'Fail while looping')

        # test indexing
        train_patients, test_patients = p[0]
        result_train, result_test = results[0]

        self.assertEqual(train_patients, result_train, 'Fail while indexing')
        self.assertEqual(test_patients, result_test, 'Fail while indexing')

    def test_dataframe_split(self):
        """
        Split a pandas.DataFrame into 5 folds
        iterate over them and try to select them by indexing
        """

        test_patient_df = pd.DataFrame.from_dict(
            {
                'patient': [1,2,2,3,4,5,5,5],
                'other_columns': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            }
        )

        results = [
            # fold 0
            (
                {
                    'patient':[1,2,2,3,5,5,5],
                    'other_columns': ['a','b','c','d','f','g','h']
                },
                {
                    'patient':[4],
                    'other_columns': ['e']
                },
            ),
            # fold 1
            (
                {
                    'patient':[1,3,4,5,5,5],
                    'other_columns': ['a','d','e','f','g','h']
                },
                {
                    'patient':[2,2],
                    'other_columns': ['b', 'c']
                },
            ),
            # fold 2
            (
                {
                    'patient':[1,2,2,4,5,5,5],
                    'other_columns': ['a','b','c','e','f','g','h']
                },
                {
                    'patient':[3],
                    'other_columns': ['d']
                },
            ),
            # fold 3
            (
                {
                    'patient':[1,2,2,3,4],
                    'other_columns': ['a','b','c','d','e']
                },
                {
                    'patient':[5,5,5],
                    'other_columns': ['f','g','h']
                },
            ),
            # fold 4
            (
                {
                    'patient':[2,2,3,4,5,5,5],
                    'other_columns': ['b','c','d','e','f','g','h']
                },
                {
                    'patient':[1],
                    'other_columns': ['a']
                },
            )
        ]

        p = PatientKFold(test_patient_df, col_patient_id='patient', random_state=42)

        # test looping
        for fold, (train_patients, test_patients) in enumerate(p):
            self.assertEqual(list(train_patients['patient']), 
                             results[fold][0]['patient'], 'Fail while looping')
            self.assertEqual(list(train_patients['other_columns']), 
                             results[fold][0]['other_columns'], 'Fail while looping')

            self.assertEqual(list(test_patients['patient']), 
                    results[fold][1]['patient'], 'Fail while looping')
            self.assertEqual(list(test_patients['other_columns']), 
                    results[fold][1]['other_columns'], 'Fail while looping')                    

        # test indexing
        train_patients, test_patients = p[0]
        result_train, result_test = results[0]

        self.assertEqual(list(train_patients['patient']), 
                            result_train['patient'], 'Fail while looping')
        self.assertEqual(list(train_patients['other_columns']), 
                            result_train['other_columns'], 'Fail while looping')

        self.assertEqual(list(test_patients['patient']), 
                result_test['patient'], 'Fail while looping')
        self.assertEqual(list(test_patients['other_columns']), 
                result_test['other_columns'], 'Fail while looping') 
 

if __name__ == '__main__':
    unittest.main()
