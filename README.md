# HBN Data Download
Scripts to download HBN dataset


## EEG download

### download_HBN_EEG_files.py
This script downloads data from the HBN data release and stores the files in a local
directory; users specify modality (EEG or MRI), Site, and release number.
Usage:
    python download_HBN_EEG_files.py -m <data modality> -s <site>
                                     -r <release number> -o <out_dir>
                                     -s <colleciotn site> -p <paradigm names>
                                     -f <file format> -rp <raw or preprocessed>
                                     -sub <Subject list to donwload> 
Example:
python download_HBN_EEG_files.py -m 'EEG' -s 'All' -r 'All' -o 'HBN_data' -p 'Video1' -f 'mat' -rp 'raw' -sub '***.csv'