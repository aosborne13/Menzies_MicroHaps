import argparse
import pandas as pd
import numpy as np
import os
import fnmatch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_to_fq', required=True, help="Path to fastq files")
    parser.add_argument('--output_file', required=True, help="Path to output meta file")
    parser.add_argument('--pattern_fw', required=True, help="pattern followed in processed forward fastq for naming")
    parser.add_argument('--pattern_rv', required=True, help="pattern followed in processed reverse fastq for naming")

    args = parser.parse_args()

    pathdir = args.path_to_fq
    odir = args.output_file
    meta_df = pd.DataFrame(columns=['id', 'ip1', 'ip2'])
    pattern_fw = args.pattern_fw
    pattern_rv = args.pattern_rv

    filelist_fw = fnmatch.filter(os.listdir(pathdir), pattern_fw)
    filelist_rv = fnmatch.filter(os.listdir(pathdir), pattern_rv)

    for entry_fw in filelist_fw:
        sampleid = entry_fw.split(pattern_fw[:-8], 1)[0]
        entry_rv = next((entry for entry in filelist_rv if sampleid in entry), None)
        
        if entry_rv:
            ipath_fw = os.path.join(pathdir, entry_fw)
            ipath_rv = os.path.join(pathdir, entry_rv)
            df = pd.DataFrame({'id': [sampleid], 'ip1': [ipath_fw], 'ip2': [ipath_rv]})
            meta_df = pd.concat([meta_df, df], ignore_index=True)

    meta_df['id'] = meta_df['id'].str.replace('_R1', '').str.replace('_R2', '')
    meta_df.to_csv(odir, sep="\t", header=False, index=False)
    print("meta file generated at " + odir)

if __name__ == "__main__":
    main()