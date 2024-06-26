import pandas as pd
import re

# Load the CSV file to examine its contents
file_path = './inputs/quaternaries_campare.csv'
data = pd.read_csv(file_path)
data.head()

# Provided elements that should have a '1' appended if missing
elements_with_one = [
    'Ag', 'Al', 'As', 'Au', 'Bi', 'Cd', 'Co', 'Cr', 'Cu', 'Fe', 'Ga', 'Ge', 'Hf', 'Hg', 'In', 'Ir', 'Mg', 'Mn', 'Mo', 'Nb',
    'Ni', 'Os', 'Pb', 'Pd', 'Pt', 'Re', 'Rh', 'Ru', 'Sb', 'Sc', 'Si', 'Sn', 'Ta', 'Te', 'Ti', 'V', 'W', 'Y', 'Zn', 'Zr'
]

def clean_element(element):
    # Remove underscore and any text after it
    element = re.sub(r'_.*', '', element)
    # Check and append '1' if necessary
    for elem in elements_with_one:
        if re.fullmatch(f"{elem}", element):
            return f"{element}1"
    return element

def edit_columns(value):
    # Parse the string into a list
    element_list = eval(value)
    # Clean each element in the list
    cleaned_list = [clean_element(elem) for elem in element_list]
    # Return the cleaned list as a string
    return str(cleaned_list)

# Apply the function to 'decomposition' and 'decomposition2' columns
data['decomposition'] = data['decomposition'].apply(edit_columns)
data['decomposition2'] = data['decomposition2'].apply(edit_columns)

# Show the modified data for verification
data[['decomposition', 'decomposition2']].head()

data.to_csv(file_path, index=False)

save = data.to_csv('out.csv', index=False)

def update_element_suffixes(dataframe, elements):
    import re

    def ensure_suffix(element_list):
        # Add a '1' suffix to elements without a number
        updated_elements = []
        for element in element_list:
            if any(char.isdigit() for char in element):  # Check if there's a digit
                updated_elements.append(element)  # Element is correct
            else:
                updated_elements.append(element + '1')  # Add '1' to elements without a suffix
        return updated_elements

    def process_decomposition_columns(column):
        # Process each row in the decomposition columns
        processed_elements = []
        for row in column:
            elements = eval(row)  # Convert string representation of list to actual list
            # Split the elements into individual chemical symbols and ensure each has a suffix
            new_elements = []
            for element in elements:
                parts = re.findall(r'[A-Z][^A-Z]*', element)  # Split into elemental parts
                corrected_elements = [part if part in elements else ensure_suffix([part])[0] for part in parts]
                new_elements.append(''.join(corrected_elements))
            processed_elements.append(new_elements)
        return processed_elements

    # List of elements to be checked
    element_list = elements

    # Apply the processing to the 'decomposition' and 'decomposition2' columns
    dataframe['decomposition'] = process_decomposition_columns(dataframe['decomposition'])
    dataframe['decomposition2'] = process_decomposition_columns(dataframe['decomposition2'])

    return dataframe

# List of elements to be checked
element_symbols = ['Ag', 'Al', 'As', 'Au', 'Bi', 'Cd', 'Co', 'Cr', 'Cu', 'Fe', 'Ga', 'Ge', 'Hf', 'Hg', 'In', 'Ir', 'Mg', 'Mn', 'Mo', 'Nb', 'Ni', 'Os', 'Pb', 'Pd', 'Pt', 'Re', 'Rh', 'Ru', 'Sb', 'Sc', 'Si', 'Sn', 'Ta', 'Te', 'Ti', 'V', 'W', 'Y', 'Zn', 'Zr']

# Apply the update function to the data
updated_data = update_element_suffixes(data.copy(), element_symbols)
updated_data.head()

save2 = updated_data.to_csv('clear_out_data.csv', index=False)