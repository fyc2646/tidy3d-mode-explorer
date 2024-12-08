import unittest
import tkinter as tk
from waveguide_gui import WaveguideGUI
import time

class TestWaveguideCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        cls.root = tk.Tk()
        cls.app = WaveguideGUI(cls.root)
        cls.root.update()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.root.destroy()
    
    def setUp(self):
        """Reset to default values before each test"""
        self.root.update()
        self._reset_to_defaults()
    
    def _reset_to_defaults(self):
        """Reset all parameters to their default values"""
        # Reset strip waveguide parameters
        self.app.core_width_var.set(0.5)
        self.app.core_thickness_var.set(0.22)
        self.app.sidewall_angle_var.set(10.0)
        
        # Reset common parameters
        self.app.core_index_var.set(3.47)
        self.app.clad_index_var.set(1.0)
        self.app.box_index_var.set(1.44)
        self.app.wavelength_var.set(1.55)
        self.app.grid_resolution_var.set(25)
        self.app.num_modes_var.set(1)
    
    def test_strip_waveguide_creation(self):
        """Test creating a strip waveguide"""
        # Set strip waveguide parameters
        self.app.waveguide_type_var.set("Strip waveguide")
        self.app._on_type_change()
        self.root.update()
        
        # Create waveguide
        waveguide = self.app._create_waveguide()
        self.assertIsNotNone(waveguide)
    
    def test_rib_waveguide_creation(self):
        """Test creating a rib waveguide"""
        # Set rib waveguide parameters
        self.app.waveguide_type_var.set("Rib waveguide")
        self.app._on_type_change()
        self.root.update()
        
        # Set slab thickness
        self.app.slab_thickness_var.set(0.1)
        
        # Create waveguide
        waveguide = self.app._create_waveguide()
        self.assertIsNotNone(waveguide)
    
    def test_slot_waveguide_creation(self):
        """Test creating a slot waveguide"""
        # Set slot waveguide parameters
        self.app.waveguide_type_var.set("Slot waveguide")
        self.app._on_type_change()
        self.root.update()
        
        # Set gap
        self.app.gap_var.set(0.1)
        
        # Create waveguide
        waveguide = self.app._create_waveguide()
        self.assertIsNotNone(waveguide)
    
    def test_local_mode_solve(self):
        """Test local mode solve functionality"""
        # Set strip waveguide parameters with known good values
        self.app.waveguide_type_var.set("Strip waveguide")
        self.app._on_type_change()
        self.root.update()
        
        # Set parameters that should give reliable results
        self.app.core_width_var.set(0.5)
        self.app.core_thickness_var.set(0.22)
        self.app.core_index_var.set(3.47)
        self.app.clad_index_var.set(1.0)
        self.app.wavelength_var.set(1.55)
        self.app.num_modes_var.set(1)
        
        # Trigger local mode solve
        self.app._solve_local_mode()
        self.root.update()
        
        # Verify that mode data was generated
        self.assertIsNotNone(self.app.mode_data)
        self.assertGreater(len(self.app.mode_data.n_eff.values[0]), 0)
        
        # Get all toplevel windows
        mode_windows = [w for w in self.app.root.winfo_children() if isinstance(w, tk.Toplevel)]
        
        # Verify that at least one mode window was created
        self.assertGreater(len(mode_windows), 0)
        
        # Verify the first mode window
        mode_window = mode_windows[0]
        self.assertTrue(mode_window.winfo_exists())
        
        # Clean up - destroy mode windows
        for window in mode_windows:
            window.destroy()

    def test_invalid_parameters(self):
        """Test waveguide creation with invalid parameters"""
        # Test with invalid core width (negative value)
        self.app.core_width_var.set(-1.0)
        waveguide = self.app._create_waveguide()
        
        # Try to solve modes (should fail)
        with self.assertRaises(Exception):
            waveguide.solve_modes()
        
        # Reset to valid value
        self.app.core_width_var.set(0.5)
        
        # Test with invalid core index (negative value)
        self.app.core_index_var.set(-1.0)
        waveguide = self.app._create_waveguide()
        
        # Try to solve modes (should fail)
        with self.assertRaises(Exception):
            waveguide.solve_modes()

if __name__ == '__main__':
    unittest.main()
