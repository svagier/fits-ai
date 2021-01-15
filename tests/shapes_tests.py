import unittest

import numpy as np

from backend.shapes import ShapesManager


class ShapesCorrectnessTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        self.__shapes_manager = ShapesManager()
        super().__init__(methodName)

    def test_number_of_shapes(self):
        correct_number_of_all_shapes = 16
        correct_number_of_initial_shapes = 4
        self.assertEqual(len(self.__shapes_manager.get_all_shapes_dict()), correct_number_of_all_shapes)
        self.assertEqual(len(self.__shapes_manager.get_names_of_initial_shapes()), correct_number_of_initial_shapes)

    def test_if_initial_shapes_in_all_shapes(self):
        for initial_shape_name in self.__shapes_manager.get_names_of_initial_shapes():
            self.assertIn(initial_shape_name, self.__shapes_manager.get_all_shapes_dict().keys())

    def test_if_shapes_contain_only_zeroes_and_ones(self):
        for all_rotations_of_shape in self.__shapes_manager.get_all_shapes_dict().values():
            for shape_rotation in all_rotations_of_shape:
                for field in np.nditer(shape_rotation):
                    self.assertIn(field, [0, 1])

    def test_if_correct_number_of_taken_fields_in_each_rotation(self):
        for all_rotations_of_shape in self.__shapes_manager.get_all_shapes_dict().values():
            number_of_ones_in_shape = int(np.sum(all_rotations_of_shape[0]))
            for shape_rotation in all_rotations_of_shape:
                self.assertEqual(number_of_ones_in_shape, int(np.sum(shape_rotation)))


if __name__ == '__main__':
    unittest.main()
