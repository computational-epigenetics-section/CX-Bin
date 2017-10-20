# Non-CpG-data-extraction
Used to filter and bin data generated by the bismark_methylation_extractor when running with the -CX flag

## Requirements
* python3

## Usage
* python CX_filtering.py [-b|--binSize BINSIZE] [-c|--context CONTEXT] [-wx] input.CX_report.txt.gz

## Input Data
* input.CX_report.txt.gz should be the CX report file generated by bismark methylation extractor when run with the -CX flag. 
This input file must be gzipped.
* The raw CX report generated by bismark will be large and contain mostly 0's. It is highly recommended that you pre-filter this file to, at the very least, remove the locations with no read coverge.

## Options
* -h,--help: Display the help message
* -b,--binSize: Specify the bin size data should be collected in - default = 200
* -c,--context: Input the cytosine context to extarct from the data, (CH, CG, CHH, CHG, C) - default = CH
* -wx: output the extracted data to a file, file will be gzipped
