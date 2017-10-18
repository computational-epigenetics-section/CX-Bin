#!/usr/bin/env python
import gzip
import sys
import os
from collections import defaultdict
from statistics import mean


def extract_context(file_path, context='CH', write_to_output=False):
    """
    :param file_path: file to be extracted, should be gzipped.
    :param context: Methylated context to extract, could be CG, CHH, CHG, CH, or C
    :param write_to_output: If true a csv file of extracted data will be generated
    :return:
    """

    # open the gzipped file and find rows with matching context
    with gzip.open(file_path, 'rt') as file:

        extracted_data = []

        if write_to_output:
            fname, ext = os.path.splitext(file_path)
            output = gzip.open(str(fname + "_" + context + '_extracted.csv.gz'), 'wt')
            output.write(",".join(['chromosome', 'location', 'strand', 'methylated_ratio', 'coverage_depth', 'context']))
            output.write("\n")

        for line in file:
            data = line.split()
            data_context = data[5]
            if context in data_context:
                chrom = data[0]
                location = data[1]
                strand = data[2]
                methyl = int(data[3])
                unmethyl = int(data[4])
                pct_methyl = methyl/(methyl+unmethyl)
                depth_coverage = methyl + unmethyl
                tri_nuc = data[6]

                out_data = [chrom, location, strand, str(pct_methyl), str(depth_coverage), tri_nuc]
                extracted_data.append(out_data)

                if write_to_output:
                    out_line = ",".join(out_data)
                    output.write(out_line)
                    output.write('\n')
        if write_to_output:
            output.close()

    return extracted_data


def bin_cx_data(extracted_data, file_name, context, bin_size = 200):
    """
    :param extracted_data: list of lists generated by extract_data()
    :param file_name: An input file name, used to generate output file name
    :return: Nothing, generates a csv output file of the binned data
    """

    bin_pct_data = defaultdict(list)
    c_in_bin = defaultdict(lambda: 0)

    for data in extracted_data:
        location = int(data[1])
        percent_methyl = data[3]
        bin_number = (location-1)//bin_size
        bin_label = (bin_number * bin_size) + bin_size
        bin_name = str(data[0][3:] + "_" + str(bin_label))

        bin_pct_data[bin_name].append(float(percent_methyl))
        c_in_bin[bin_name] += 1

    fname, ext = os.path.splitext(file_name)

    with open(str(fname + "_" + context +'_bins.csv'), 'w') as output:
        header = ",".join(['Bin Name', 'Avg Methylation', str(context + "s in bin")])
        output.write(header)
        output.write("\n")
        for key in list(bin_pct_data.keys()):
            # chromosome = key.split("_")[0]
            output_bin_name = "chr" + str(key)
            output_bin_pct_methyl = mean(bin_pct_data[key])
            output_c_in_bin = c_in_bin[key]
            out_line = ",".join([output_bin_name, str(output_bin_pct_methyl), str(output_c_in_bin)])
            output.write(out_line)
            output.write("\n")


if __name__ == "__main__":

    # todo set up argument parser for input_file, extraction_output_writing, bin_size
    input_file = sys.argv[1] # change later to use arg parser
    c_context = 'CH'
    filename, extension = os.path.splitext(input_file)
    if extension != '.gz':
        raise ValueError("Make sure your file is gzipped and has extension .gz"
                         )
    ext_data = extract_context(sys.argv[1], write_to_output=True, context=c_context)
    bin_cx_data(ext_data, filename, c_context, bin_size=200)
