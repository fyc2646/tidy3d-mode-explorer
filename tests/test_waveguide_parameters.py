import unittest
import tkinter as tk
from waveguide_gui import WaveguideGUI

class TestWaveguideParameters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        cls.root = tk.Tk()
        cls.app = WaveguideGUI(cls.root)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.root.destroy()
    
    def test_initial_values(self):
        """Test initial parameter values"""
        # Test strip waveguide parameters
        self.assertEqual(self.app.core_width_var.get(), 0.5)
        self.assertEqual(self.app.core_thickness_var.get(), 0.22)
        self.assertEqual(self.app.sidewall_angle_var.get(), 10.0)
        
        # Test common parameters
        self.assertEqual(self.app.core_index_var.get(), 3.47)
        self.assertEqual(self.app.clad_index_var.get(), 1.0)
        self.assertEqual(self.app.box_index_var.get(), 1.44)
        self.assertEqual(self.app.wavelength_var.get(), 1.55)
        self.assertEqual(self.app.grid_resolution_var.get(), 25)
        self.assertEqual(self.app.num_modes_var.get(), 1)
    
    def test_waveguide_type_change(self):
        """Test changing waveguide type"""
        # Initially should be Strip waveguide
        self.assertEqual(self.app.waveguide_type_var.get(), "Strip waveguide")
        
        # Change to Rib waveguide
        self.app.type_combobox.set("Rib waveguide")
        self.app._on_type_change()
        self.assertEqual(self.app.waveguide_type_var.get(), "Rib waveguide")
        
        # Change to Slot waveguide
        self.app.type_combobox.set("Slot waveguide")
        self.app._on_type_change()
        self.assertEqual(self.app.waveguide_type_var.get(), "Slot waveguide")
    
    def test_validate_float(self):
        """Test float validation"""
        # Test valid inputs
        self.assertTrue(self.app._validate_float_or_empty("123"))
        self.assertTrue(self.app._validate_float_or_empty("123.456"))
        self.assertTrue(self.app._validate_float_or_empty("-123.456"))
        self.assertTrue(self.app._validate_float_or_empty(""))
        
        # Test invalid inputs
        self.assertFalse(self.app._validate_float_or_empty("abc"))
        self.assertFalse(self.app._validate_float_or_empty("12.34.56"))
        self.assertFalse(self.app._validate_float_or_empty("12abc"))

if __name__ == '__main__':
    unittest.main()
