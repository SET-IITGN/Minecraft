def extract_lines(file_path, line_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # print(lines)
    extracted_lines = []
    start_index = line_number - 1  # Adjust for zero-based indexing
    end_index = line_number

    # Extract lines above the given line number
    for i in range(start_index, -1, -1):
        line = lines[i]
        if 'def' in line or line.startswith('class') or line.startswith('"""'):
            line = str(i+1) + ' ' + line
            extracted_lines.insert(0, line)
            break
        line = str(i+1) + ' ' + line
        extracted_lines.insert(0, line)

    # Extract lines below the given line number
    for i in range(end_index, len(lines)):
        line = lines[i]
        if 'def' in line or line.startswith('class') or line.startswith('if __name__'):
            break
        line = str(i+1) + ' ' + line
        extracted_lines.append(line)

    return ''.join(extracted_lines)

# # Example usage
# file_path = '/home/saikrishna/Documents/pyVulEvo/ASE/2023/geocoder/geocoder/bing.py'  # Replace with your file path
# line_number = 7
#   # Replace with your desired line number

# lines = extract_lines(file_path, line_number)
# for line in lines:
#     print(line)ines = extract_lines(file_path, line_number)
# for line in lines:
#     print(l