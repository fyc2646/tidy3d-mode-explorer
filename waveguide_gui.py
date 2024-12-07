# -*- coding: utf-8 -*-
import tkinter as tk
import math
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tidy3d import Medium, ModeSpec
from tidy3d.plugins.waveguide import RectangularDielectric
from tidy3d.plugins.mode.web import run as run_mode_solver
import traceback

class WaveguideGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tidy3D Waveguide Designer")
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left frame for inputs
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Create right frame for plot
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Create figure for plot
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create waveguide type selection
        self.type_frame = ttk.LabelFrame(self.left_frame, text="Waveguide Type")
        self.type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.waveguide_type_var = tk.StringVar(value="Strip waveguide")
        self.type_combobox = ttk.Combobox(
            self.type_frame, 
            textvariable=self.waveguide_type_var,
            values=["Strip waveguide", "Rib waveguide", "Slot waveguide"],
            state="readonly"
        )
        self.type_combobox.pack(fill=tk.X, padx=5, pady=5)
        self.type_combobox.bind('<<ComboboxSelected>>', lambda e: self._on_type_change())
        
        # Create strip waveguide parameters frame
        self.strip_frame = ttk.LabelFrame(self.left_frame, text="Strip Waveguide Parameters")
        self.strip_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.strip_frame, text="Core Width (um):").grid(row=0, column=0, padx=5, pady=5)
        self.core_width_var = tk.DoubleVar(value=0.5)
        ttk.Entry(self.strip_frame, textvariable=self.core_width_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.strip_frame, text="Core Thickness (um):").grid(row=1, column=0, padx=5, pady=5)
        self.core_thickness_var = tk.DoubleVar(value=0.22)
        ttk.Entry(self.strip_frame, textvariable=self.core_thickness_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.strip_frame, text="Sidewall Angle (deg):").grid(row=2, column=0, padx=5, pady=5)
        self.sidewall_angle_var = tk.DoubleVar(value=10.0)
        ttk.Entry(self.strip_frame, textvariable=self.sidewall_angle_var).grid(row=2, column=1, padx=5, pady=5)
        
        # Create rib waveguide parameters frame
        self.rib_frame = ttk.LabelFrame(self.left_frame, text="Rib Waveguide Parameters")
        
        ttk.Label(self.rib_frame, text="Core Width (um):").grid(row=0, column=0, padx=5, pady=5)
        self.rib_width_var = tk.DoubleVar(value=0.5)
        ttk.Entry(self.rib_frame, textvariable=self.rib_width_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.rib_frame, text="Core Thickness (um):").grid(row=1, column=0, padx=5, pady=5)
        self.rib_thickness_var = tk.DoubleVar(value=0.22)
        ttk.Entry(self.rib_frame, textvariable=self.rib_thickness_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.rib_frame, text="Sidewall Angle (deg):").grid(row=2, column=0, padx=5, pady=5)
        self.rib_angle_var = tk.DoubleVar(value=10.0)
        ttk.Entry(self.rib_frame, textvariable=self.rib_angle_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.rib_frame, text="Slab Thickness (um):").grid(row=3, column=0, padx=5, pady=5)
        self.slab_thickness_var = tk.DoubleVar(value=0.1)
        ttk.Entry(self.rib_frame, textvariable=self.slab_thickness_var).grid(row=3, column=1, padx=5, pady=5)
        
        # Create slot waveguide parameters frame
        self.slot_frame = ttk.LabelFrame(self.left_frame, text="Slot Waveguide Parameters")
        
        ttk.Label(self.slot_frame, text="First Core Width (um):").grid(row=0, column=0, padx=5, pady=5)
        self.first_core_width_var = tk.DoubleVar(value=0.5)
        ttk.Entry(self.slot_frame, textvariable=self.first_core_width_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.slot_frame, text="Second Core Width (um):").grid(row=1, column=0, padx=5, pady=5)
        self.second_core_width_var = tk.DoubleVar(value=0.5)
        ttk.Entry(self.slot_frame, textvariable=self.second_core_width_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.slot_frame, text="Gap (um):").grid(row=2, column=0, padx=5, pady=5)
        self.gap_var = tk.DoubleVar(value=0.1)
        ttk.Entry(self.slot_frame, textvariable=self.gap_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.slot_frame, text="Core Thickness (um):").grid(row=3, column=0, padx=5, pady=5)
        self.slot_thickness_var = tk.DoubleVar(value=0.22)
        ttk.Entry(self.slot_frame, textvariable=self.slot_thickness_var).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self.slot_frame, text="Sidewall Angle (deg):").grid(row=4, column=0, padx=5, pady=5)
        self.slot_angle_var = tk.DoubleVar(value=10.0)
        ttk.Entry(self.slot_frame, textvariable=self.slot_angle_var).grid(row=4, column=1, padx=5, pady=5)
        
        # Create common parameters frame
        self.common_frame = ttk.LabelFrame(self.left_frame, text="Common Parameters")
        self.common_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Core Index:").grid(row=0, column=0, padx=5, pady=5)
        self.core_index_var = tk.DoubleVar(value=3.47)
        ttk.Entry(self.common_frame, textvariable=self.core_index_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Clad Index:").grid(row=1, column=0, padx=5, pady=5)
        self.clad_index_var = tk.DoubleVar(value=1.0)
        ttk.Entry(self.common_frame, textvariable=self.clad_index_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Box Index:").grid(row=2, column=0, padx=5, pady=5)
        self.box_index_var = tk.DoubleVar(value=1.44)
        ttk.Entry(self.common_frame, textvariable=self.box_index_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Clad Thickness (um):").grid(row=3, column=0, padx=5, pady=5)
        self.clad_thickness_var = tk.DoubleVar(value=2.0)
        ttk.Entry(self.common_frame, textvariable=self.clad_thickness_var).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Box Thickness (um):").grid(row=4, column=0, padx=5, pady=5)
        self.box_thickness_var = tk.DoubleVar(value=2.0)
        ttk.Entry(self.common_frame, textvariable=self.box_thickness_var).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Wavelength (um):").grid(row=5, column=0, padx=5, pady=5)
        self.wavelength_var = tk.DoubleVar(value=1.55)
        ttk.Entry(self.common_frame, textvariable=self.wavelength_var).grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Grid Resolution:").grid(row=6, column=0, padx=5, pady=5)
        self.grid_resolution_var = tk.DoubleVar(value=25)
        ttk.Entry(self.common_frame, textvariable=self.grid_resolution_var).grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Number of Modes:").grid(row=7, column=0, padx=5, pady=5)
        self.num_modes_var = tk.IntVar(value=1)
        ttk.Entry(self.common_frame, textvariable=self.num_modes_var).grid(row=7, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Target n_eff:").grid(row=8, column=0, padx=5, pady=5)
        self.target_neff_entry = ttk.Entry(self.common_frame, width=10, validate='key', validatecommand=(self.root.register(self._validate_float_or_empty), '%P'))
        self.target_neff_entry.grid(row=8, column=1, padx=5, pady=5)
        
        vcmd = (self.root.register(self._validate_float_or_empty), '%P')
        ttk.Label(self.common_frame, text="Bend Radius (um):").grid(row=9, column=0, padx=5, pady=5)
        self.bend_radius_entry = ttk.Entry(self.common_frame, width=10, validate='key', validatecommand=vcmd)
        self.bend_radius_entry.grid(row=9, column=1, padx=5, pady=5)
        
        ttk.Label(self.common_frame, text="Use PML:").grid(row=10, column=0, padx=5, pady=5)
        self.use_pml_var = tk.StringVar(value="False")
        pml_combo = ttk.Combobox(self.common_frame, textvariable=self.use_pml_var, values=["True", "False"], width=7, state="readonly")
        pml_combo.grid(row=10, column=1, padx=5, pady=5)
        pml_combo.set("False")
        
        # Create simulation parameters frame
        self.sim_frame = ttk.LabelFrame(self.left_frame, text="Simulation Parameters")
        self.sim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create buttons
        self.button_frame = ttk.Frame(self.left_frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(self.button_frame, text="Plot", command=self._update_plot).pack(side=tk.LEFT, padx=5)
        
        # Create solve buttons frame
        solve_frame = ttk.Frame(self.button_frame)
        solve_frame.pack(side=tk.LEFT, padx=5)
        
        # Add Local mode solve button
        ttk.Button(
            solve_frame,
            text="Local mode solve",
            command=self._solve_local_mode
        ).pack(side=tk.LEFT, padx=5)
        
        # Add Server mode solve button
        ttk.Button(
            solve_frame,
            text="Server mode solve",
            command=self._solve_server_mode
        ).pack(side=tk.LEFT, padx=5)
        
        # Store mode data
        self.mode_data = None
        self.current_waveguide = None
        self.current_mode_index = 0
        self.current_colorbar = None  # Store reference to current colorbar
        
        # Show initial waveguide type
        self._on_type_change()
        
    def _on_type_change(self):
        waveguide_type = self.waveguide_type_var.get()
        
        # Hide all parameter frames
        self.strip_frame.pack_forget()
        self.rib_frame.pack_forget()
        self.slot_frame.pack_forget()
        
        # Show the selected parameter frame
        if waveguide_type == "Strip waveguide":
            self.strip_frame.pack(after=self.type_frame, fill=tk.X, padx=5, pady=5)
        elif waveguide_type == "Rib waveguide":
            self.rib_frame.pack(after=self.type_frame, fill=tk.X, padx=5, pady=5)
        else:  # Slot waveguide
            self.slot_frame.pack(after=self.type_frame, fill=tk.X, padx=5, pady=5)
        
        # Update the plot
        self._update_plot()
    
    def _create_waveguide(self):
        try:
            # Create materials
            core = Medium(permittivity=self.core_index_var.get()**2)
            clad = Medium(permittivity=self.clad_index_var.get()**2)
            box = Medium(permittivity=self.box_index_var.get()**2)
            
            # Get common parameters
            wavelength = self.wavelength_var.get()
            grid_resolution = self.grid_resolution_var.get()
            num_modes = self.num_modes_var.get()
            
            # Get bend radius (None if empty or invalid)
            bend_radius = self._get_bend_radius()
            
            # Get target n_eff (None if empty or invalid)
            target_neff = self._get_target_neff()
            
            # Get PML setting
            use_pml = self.use_pml_var.get() == "True"
            num_pml = (12, 12) if use_pml else (0, 0)
            
            # Create mode specification
            mode_spec_params = {
                'num_modes': num_modes,
                'bend_radius': bend_radius,
                'num_pml': num_pml,
                'group_index_step': True,
                'precision': 'double'
            }
            
            # Add optional parameters
            if target_neff is not None:
                mode_spec_params['target_neff'] = target_neff
            
            if bend_radius is not None:
                mode_spec_params['bend_axis'] = 1
            
            mode_spec = ModeSpec(**mode_spec_params)
            
            # Get parameters based on waveguide type
            waveguide_type = self.waveguide_type_var.get()
            
            if waveguide_type == "Strip waveguide":
                width = self.core_width_var.get()
                thickness = self.core_thickness_var.get()
                sidewall_angle_rad = math.radians(self.sidewall_angle_var.get())
                slab_thickness = 0.0
                gap = 0.0
            elif waveguide_type == "Rib waveguide":
                width = self.rib_width_var.get()
                thickness = self.rib_thickness_var.get()
                sidewall_angle_rad = math.radians(self.rib_angle_var.get())
                slab_thickness = self.slab_thickness_var.get()
                gap = 0.0
            else:  # Slot waveguide
                width = [self.first_core_width_var.get(), self.second_core_width_var.get()]
                thickness = self.slot_thickness_var.get()
                sidewall_angle_rad = math.radians(self.slot_angle_var.get())
                slab_thickness = 0.0
                gap = self.gap_var.get()
            
            # Create waveguide
            waveguide = RectangularDielectric(
                core_width=width,
                core_thickness=thickness,
                wavelength=wavelength,
                core_medium=core,
                clad_medium=clad,
                box_medium=box,
                clad_thickness=self.clad_thickness_var.get(),
                box_thickness=self.box_thickness_var.get(),
                slab_thickness=slab_thickness,
                sidewall_angle=sidewall_angle_rad,
                gap=gap,
                mode_spec=mode_spec,
                grid_resolution=grid_resolution,
            )
            
            return waveguide
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
            return None
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
    
    def _update_plot(self):
        waveguide = self._create_waveguide()
        if waveguide is None:
            return
        
        try:
            # Clear the plot
            self.ax.clear()
            
            # Plot the waveguide
            waveguide.mode_solver.plot(ax=self.ax)
            
            # Update the canvas
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Plot Error", str(e))
    
    def _create_mode_window(self, mode_index, mode_data):
        """Create a window displaying mode properties and field plot."""
        # Create new window for this mode
        mode_window = tk.Toplevel(self.root)
        mode_window.title("Mode {}".format(mode_index))
        
        # Create frame for mode properties
        props_frame = ttk.Frame(mode_window)
        props_frame.pack(pady=5, padx=10, fill=tk.X)
        
        # Get mode properties
        n_eff = float(mode_data.n_eff.values[0][mode_index])
        k_eff = float(mode_data.k_eff.values[0][mode_index])
        n_group = float(mode_data.n_group.values[0][mode_index])
        te_frac = float(mode_data.pol_fraction.te.values[0][mode_index])
        tm_frac = float(mode_data.pol_fraction.tm.values[0][mode_index])
        mode_area = float(mode_data.mode_area.values[0][mode_index])
        
        # Create labels for properties
        props = [
            ("n_eff", "{:.6f}".format(n_eff)),
            ("k_eff", "{:.6f}".format(k_eff)),
            ("Group Index", "{:.6f}".format(n_group)),
            ("TE Fraction", "{:.1f}%".format(te_frac * 100)),
            ("TM Fraction", "{:.1f}%".format(tm_frac * 100)),
            ("Mode Area", "{:.2f} um²".format(mode_area))
        ]
        
        # Add properties to frame
        for i, (label, value) in enumerate(props):
            ttk.Label(props_frame, text=f"{label}:").grid(row=i, column=0, sticky='e', padx=5, pady=2)
            ttk.Label(props_frame, text=value).grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
        # Create figure and canvas for field plot
        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, master=mode_window)
        canvas.get_tk_widget().pack(pady=5)
        
        # Plot field for this mode
        self.current_waveguide.plot_field(
            field_name="E",
            val="abs",
            mode_index=mode_index,
            ax=ax
        )
        canvas.draw()
    
    def _solve_local_mode(self):
        try:
            # Create the waveguide
            self.current_waveguide = self._create_waveguide()
            if self.current_waveguide is None:
                return
                
            # Solve for modes
            self.mode_data = self.current_waveguide.mode_solver.solve()
            
            # Create a window for each mode
            for mode_index in range(len(self.mode_data.n_eff.values[0])):
                self._create_mode_window(mode_index, self.mode_data)
            
        except Exception as e:
            print("Error in local mode solve:", str(e))
            print("Full error:", traceback.format_exc())
            messagebox.showerror("Error", str(e))
    
    def _solve_server_mode(self):
        try:
            # Create the waveguide
            self.current_waveguide = self._create_waveguide()
            if self.current_waveguide is None:
                return
                
            # Create progress window
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Server Mode Solve")
            progress_window.geometry("300x80")
            progress_window.transient(self.root)
            progress_window.grab_set()  # Make the window modal
            
            # Center the progress window
            window_width = 300
            window_height = 80
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            progress_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Add message
            message = tk.Label(progress_window, text="Solving modes on server...\nThis may take a few moments.")
            message.pack(expand=True)
            
            # Solve for modes using server
            try:
                # Update the GUI
                progress_window.update()
                
                # Run the solver
                self.mode_data = run_mode_solver(self.current_waveguide.mode_solver)
                
                # Close progress window
                progress_window.destroy()
                
                # Create a window for each mode
                for mode_index in range(len(self.mode_data.n_eff.values[0])):
                    self._create_mode_window(mode_index, self.mode_data)
                
            except Exception as server_error:
                # Close progress window if there's an error
                progress_window.destroy()
                print("Error during server mode solve:", str(server_error))
                print("Full server error:", traceback.format_exc())
                messagebox.showerror("Server Error", "Error during server mode solve: {}".format(str(server_error)))
                return
            
        except Exception as e:
            print("Error in server mode solve:", str(e))
            print("Full error:", traceback.format_exc())
            messagebox.showerror("Error", str(e))
    
    def _reset_values(self):
        # Reset to default values
        self.waveguide_type_var.set("Strip waveguide")
        self._on_type_change()
        
        # Strip waveguide parameters
        self.core_width_var.set(0.5)
        self.core_thickness_var.set(0.22)
        self.sidewall_angle_var.set(10.0)
        
        # Rib waveguide parameters
        self.rib_width_var.set(0.5)
        self.rib_thickness_var.set(0.22)
        self.rib_angle_var.set(10.0)
        self.slab_thickness_var.set(0.1)
        
        # Slot waveguide parameters
        self.first_core_width_var.set(0.5)
        self.second_core_width_var.set(0.5)
        self.gap_var.set(0.1)
        self.slot_thickness_var.set(0.22)
        self.slot_angle_var.set(10.0)
        
        # Common parameters
        self.core_index_var.set(3.47)
        self.clad_index_var.set(1.0)
        self.box_index_var.set(1.44)
        self.clad_thickness_var.set(2.0)
        self.box_thickness_var.set(2.0)
        
        # Simulation parameters
        self.wavelength_var.set(1.55)
        self.grid_resolution_var.set(25)
        self.num_modes_var.set(1)
        
        self._update_plot()

    def _validate_float_or_empty(self, value):
        """Validate if the input is either empty or a valid float."""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
            
    def _get_bend_radius(self):
        """Get bend radius value, returns None if empty or invalid."""
        value = self.bend_radius_entry.get().strip()
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None
            
    def _get_target_neff(self):
        """Get target n_eff value, returns None if empty or invalid."""
        value = self.target_neff_entry.get().strip()
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None
            
if __name__ == "__main__":
    root = tk.Tk()
    app = WaveguideGUI(root)
    root.mainloop()
