# HBN Data Download
Scripts to download HBN dataset


## download_HBN_EEG_files.py  EEG Indivisual File downlaod

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


A same vertiosn but works on Windows:
python download_HBN_EEG_files_Windows.py -m EEG -s All -r All -o HBN_data -p Video1 -f mat -rp raw


## download_HBN_EEG_files.py  EEG Indivisual File downlaod

