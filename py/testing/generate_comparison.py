import argparse
import parse_output_data

def main():
    # arg parsing
    parser = argparse.ArgumentParser(description="Compare Fortran and Python results by parsing and plotting data.")
    parser.add_argument("fortran_file", type=str, help="Path to the Fortran-generated data file")
    parser.add_argument("python_file", type=str, help="Path to the Python-generated data file")
    parser.add_argument("--output_plot", type=str, default="comparison_plot.png", help="Name of the output plot file")

    args = parser.parse_args()

    # Define output CSV filenames
    fortran_csv = "FORTRAN_parsed_sac.csv"
    python_csv = "PYTHON_parsed_sac.csv"

    # Parse and save the data
    print(f"Parsing Fortran file: {args.fortran_file} -> {fortran_csv}")
    parse_output_data.parse_and_save_csv(args.fortran_file, fortran_csv)

    print(f"Parsing Python file: {args.python_file} -> {python_csv}")
    parse_output_data.parse_and_save_csv(args.python_file, python_csv)

    # Generate plot
    print(f"Generating comparison plot: {args.output_plot}")
    parse_output_data.plot_data_from_csv(fortran_csv, python_csv, args.output_plot)

if __name__ == "__main__":
    main()
