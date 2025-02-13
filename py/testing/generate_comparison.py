import parse_output_data

# Parse the original data files into CSV format
parse_output_data.parse_and_save_csv("FORTRAN_example_sac.dat", "FORTRAN_parsed_sac.csv")
parse_output_data.parse_and_save_csv("PYTHON_example_sac.dat", "PYTHON_parsed_sac.csv")

# Generate and save the plot
parse_output_data.plot_data_from_csv("FORTRAN_parsed_sac.csv", "PYTHON_parsed_sac.csv", "comparison_plot.png")


