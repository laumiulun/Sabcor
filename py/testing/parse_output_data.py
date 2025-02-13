import pandas as pd
import matplotlib.pyplot as plt

def parse_and_save_csv(input_file_path, output_file_path):
    """
    Parses a text file containing numerical data with metadata comments (output from Sabcor),
    extracts the numerical data, and saves it in a CSV file with two columns.
    
    Parameters:
        input_file_path (str): Path to the input text file.
        output_file_path (str): Path to save the output CSV file.
    """
    # Read the file contents
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    # Find the start of the data section
    data_start_index = None
    for index, line in enumerate(lines):
        if not line.strip().startswith('#'):
            data_start_index = index
            break
    
    # Extract and clean the data
    if data_start_index is not None:
        data_lines = lines[data_start_index:]
    else:
        data_lines = []
    
    parsed_data = [
        line.strip() for line in data_lines if line.strip() and not line.strip().startswith('#')
    ]
    
    # Split the cleaned data into two columns
    data_pairs = [line.split() for line in parsed_data]
    
    # Create a DataFrame
    df = pd.DataFrame(data_pairs, columns=["Column1", "Column2"])
    
    # Save to CSV
    df.to_csv(output_file_path, index=False)
    
    print(f"Data saved to {output_file_path}")


def plot_data_from_csv(file1, file2, output_image="FvsPy.png"):
    """
    Reads two CSV files, extracts their first two columns, and overlays their plots.

    Parameters:
    - file1: str, path to the first CSV file (Fortran data)
    - file2: str, path to the second CSV file (Python data)
    - output_image: str, name of the output image file

    The function assumes that each CSV file has at least two columns of numerical data.
    """
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Extract the first two columns from each file
    X_F, Y_F = df1.iloc[:, 0], df1.iloc[:, 1]  # First file (Fortran data)
    X_Py, Y_Py = df2.iloc[:, 0], df2.iloc[:, 1]  # Second file (Python data)

    # Plotting the data
    plt.figure(figsize=(8, 6))
    
    # First dataset (solid line)
    plt.plot(X_F, Y_F, label="Fortran", linewidth=2)

    # Second dataset (dashed line)
    plt.plot(X_Py, Y_Py, label="Python", linestyle='--', linewidth=2)

    # Adding labels, legend, and title
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    plt.title("Overlayed Plot of Fortran and Python Result")
    plt.legend()
    plt.grid()

    # Save and show the plot
    plt.savefig(output_image)
    plt.show()


