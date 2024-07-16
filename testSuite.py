import unittest
import os
from unittest.mock import patch, mock_open, MagicMock
from src.Machines.Savannah.Pressure import Pressure  # Assuming the class is in a file named pressure_module.py

class TestPressure(unittest.TestCase):
    def setUp(self):
        self.data_path = "test_data"
        self.pressure = Pressure(self.data_path)
        # Create necessary test directories
        os.makedirs(self.pressure.pressureDirPath, exist_ok=True)
        os.makedirs(self.pressure.plotpath, exist_ok=True)
        os.makedirs(self.pressure.textpath, exist_ok=True)

    def tearDown(self):
        # Clean up any files or directories created for the tests
        if os.path.exists(self.data_path):
            for root, dirs, files in os.walk(self.data_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.data_path)

    def test_initialization(self):
        self.assertEqual(self.pressure.dataPath, self.data_path)
        self.assertEqual(self.pressure.pTime, [])
        self.assertEqual(self.pressure.Pressure, [])
        self.assertEqual(self.pressure.cycles, [])
        self.assertEqual(self.pressure.pressureDirPath, self.data_path + "/Pressure-Data")
        self.assertEqual(self.pressure.plotpath, self.data_path + "/Output_Plots")
        self.assertEqual(self.pressure.textpath, self.data_path + "/Output_Text")

    @patch('os.listdir', return_value=['test_file.txt'])
    def test_readDir(self, mock_listdir):
        self.pressure.readDir()
        self.assertIn('test_file.txt', self.pressure.dir_list)

    @patch('builtins.open', new_callable=mock_open, read_data="100 0.01 1 RecipeName\n")
    def test_readFile(self, mock_file):
        self.pressure.pressureFilePath = 'test_file.txt'
        self.pressure.readFile()
        self.assertEqual(self.pressure.pTime, [100.0])
        self.assertEqual(self.pressure.Pressure, [0.01])
        self.assertEqual(self.pressure.cycles, [1])
        self.assertEqual(self.pressure.recipe, 'RecipeName')

    @patch('os.remove')
    @patch('matplotlib.pyplot.figure')
    def test_plotPressure(self, mock_figure, mock_remove):
        self.pressure.pTime = [1, 2, 3, 4, 5]
        self.pressure.Pressure = [0.1, 0.2, 0.3, 0.4, 0.5]
        self.pressure.plotPressure()
        mock_figure().savefig.assert_called_once_with(self.pressure.plotpath + "/PressureData.png")

    def test_genReport(self):
        self.pressure.pTime = [100.0]
        self.pressure.Pressure = [0.01]
        self.pressure.cycles = [1]
        self.pressure.recipe = 'RecipeName'
        report = self.pressure.genReport()
        self.assertIn("PRESSURE REPORT", report)
        self.assertIn("Recipe: RECIPENAME", report)
        self.assertTrue(os.path.exists(self.pressure.textpath + "/Pressure Report.txt"))

    @patch('os.path.getctime', return_value=0)
    @patch('os.listdir', return_value=['test_file.txt'])
    def test_initialize(self, mock_listdir, mock_getctime):
        self.pressure.initialize()
        self.assertEqual(self.pressure.pressureFilePath, self.pressure.pressureDirPath + '/test_file.txt')

    @patch('builtins.open', new_callable=mock_open, read_data="test_file_path\n")
    def test_sendData(self, mock_file):
        self.pressure.pressureFilePath = 'test_file_path'
        with patch.object(self.pressure, 'genReport', return_value=None):
            with patch.object(self.pressure, 'plotPressure', return_value=None):
                result = self.pressure.sendData()
                self.assertTrue(result)
                mock_file().write.assert_called_with('test_file_path\n')

if __name__ == "__main__":
    unittest.main()
