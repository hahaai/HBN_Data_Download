# HBN Data Download
Scripts to download HBN dataset


## download_HBN_EEG_files.py : EEG Indivisual files downlaod

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


## download_HBN_EEG_tars.py : EEG tar files downlaod

This script downloads data from the HBN data release and stores the files in a local
directory; users specify modality (EEG or MRI), Site, and release number.

Usage:

    python download_HBN_tars.py -m <data modality>

                                -s <site>

                                -r <release number> 

                                -o <out_dir>

Example:

python download_HBN_tars.py -m 'EEG' -s 'All' -r 'R3' -o 'HBN_data'


## download_HBN_MRI_files.sh : 

This script downlaods MRI data.

OPTIONS: Dataout path, 

         Data type to download: T1w, T2w, MT-on, MT-off, dwi, fmap, peer, rest, movieDM, movieTP

         Site to download: SI, RU, CBIC or All. * All will download the data from all sites

         Subject list path to download: optional. A text file with subject names (NDAR***) to download  

  REQUIREMENTS:  AWS CLI:https://aws.amazon.com/cli/

USAGE:  

./bash MRI_S3_downloader.sh ~/Downloads/HBM_MRI 'dwi' 'All' 'sublist.txt'


