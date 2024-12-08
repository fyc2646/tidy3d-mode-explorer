import unittest
import tkinter as tk
from waveguide_gui import WaveguideGUI

class TestUIComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        cls.root = tk.Tk()
        cls.app = WaveguideGUI(cls.root)
        cls.root.update()  # Process all pending events
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.root.destroy()
    
    def setUp(self):
        """Set up before each test"""
        self.root.update()  # Process all pending events
    
    def test_frame_visibility(self):
        """Test frame visibility when changing waveguide types"""
        # Test Strip waveguide
        self.app.waveguide_type_var.set("Strip waveguide")
        self.app._on_type_change()
        self.root.update()
        self.assertTrue(self.app.strip_frame.winfo_ismapped())
        self.assertFalse(self.app.rib_frame.winfo_ismapped())
        self.assertFalse(self.app.slot_frame.winfo_ismapped())
        
        # Test Rib waveguide
        self.app.waveguide_type_var.set("Rib waveguide")
        self.app._on_type_change()
        self.root.update()
        self.assertFalse(self.app.strip_frame.winfo_ismapped())
        self.assertTrue(self.app.rib_frame.winfo_ismapped())
        self.assertFalse(self.app.slot_frame.winfo_ismapped())
        
        # Test Slot waveguide
        self.app.waveguide_type_var.set("Slot waveguide")
        self.app._on_type_change()
        self.root.update()
        self.assertFalse(self.app.strip_frame.winfo_ismapped())
        self.assertFalse(self.app.rib_frame.winfo_ismapped())
        self.assertTrue(self.app.slot_frame.winfo_ismapped())
    
    def test_common_frame_always_visible(self):
        """Test that common parameters frame is always visible"""
        # Test visibility for each waveguide type
        for waveguide_type in ["Strip waveguide", "Rib waveguide", "Slot waveguide"]:
            self.app.waveguide_type_var.set(waveguide_type)
            self.app._on_type_change()
            self.root.update()
            self.assertTrue(self.app.common_frame.winfo_ismapped())
    
    def test_entry_validation(self):
        """Test entry field validation"""
        # Test target n_eff entry
        self.assertTrue(self.app._validate_float_or_empty("1.5"))
        self.assertTrue(self.app._validate_float_or_empty(""))
        self.assertFalse(self.app._validate_float_or_empty("abc"))
        
        # Test bend radius entry
        self.assertTrue(self.app._validate_float_or_empty("100"))
        self.assertTrue(self.app._validate_float_or_empty(""))
        self.assertFalse(self.app._validate_float_or_empty("abc"))

if __name__ == '__main__':
    unittest.main()
