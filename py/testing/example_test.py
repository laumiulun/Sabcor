from sabcor import Sabcor

# Initialize the object with input data and optional parameter file
sabcor_processor = Sabcor("example.dat", "sab.inp")

# Run the processing pipeline
output_filename = sabcor_processor.process()

print(f"Output file generated: {output_filename}")
