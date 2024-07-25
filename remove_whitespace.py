import json

def remove_whitespace_from_large_json(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        curline = 0
        for line in infile:
            curline += 1
            print(curline)
            # Remove leading and trailing whitespace from each line
            stripped_line = line.strip()
            # Remoe 2 below
            outfile.write(stripped_line)
            outfile.write('\n')
            #if stripped_line:  # Only write non-empty lines
            #    json_obj = json.loads(stripped_line)
            #    json.dump(json_obj, outfile, separators=(',', ':'))
            #    outfile.write('\n')

input_file = 'index.json'
output_file = 'compressed_output.json'

remove_whitespace_from_large_json(input_file, output_file)
