import unittest

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


if __name__ == '__main__':
    unittest.main()
