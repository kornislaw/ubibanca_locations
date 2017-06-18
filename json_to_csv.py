import csv, json


def json_to_csv(input_filename, output_filename):
    """ Converts data from a flat JSON file to CSV format.
        Note it works well only for flat JSON structures, no nested data. 
    """
    input_file = open(input_filename)
    data = json.load(input_file)
    input_file.close()

    with open(output_filename, 'w') as csvfile:
        output = csv.writer(csvfile)
        output.writerow(data[0].keys())  # header row

        for row in data:
            output.writerow(row.values())
