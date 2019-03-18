# download_HBN_EEG_files.py
#
# Author: Lei Ai, CMI 2018
# Nov, 2018. Modification: Added an opiton -sub to allow specifying a subject list to download, instead of the whole list.

'''
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
'''


# Main collect and download function
def collect_and_download(modality, release_num, site, paradigm, format, raw_preprocessed, out_dir,sublist_path):

    '''
    Function to collect and download images from the ABIDE preprocessed
    directory on FCP-INDI's S3 bucket
    Parameters
    ----------
    -m modality : string
        EEG
    -r release_num : string
        R1, R2,  R3, All
    -s site : string
        All
    -p paradigm : string
        RestingState, SAIIT_2AFC_Block1, SAIIT_2AFC_Block2, SAIIT_2AFC_Block3, SurroundSupp_Block1, SurroundSupp_Block2, Video1, Video2, Video3, WISC_ProcSpeed, vis_learn
    -f dataformat : string
        mat or csv
    -rp raw_preprocessed : string
        raw or preprocessed
    -sub subject_list : string
        The full path of a csv file with subject to download. 
    -o : string
        filepath to a local directory to save files to
    Returns
    -------
    None
        this function does not return a value; it downloads data from
        S3 to a local directory

    '''
    
    # Import packages
    import os
    import urllib
    import pandas as pd

    if modality == 'MRI' and site == 'All' or site == 'all' or site == 'ALL':
        site_list=['SI','RU','CBIC']
    else:
        site_list=[site]

    for site in site_list:
        # Init variables
        s3_prefix = 'https://s3.amazonaws.com/fcp-indi/data/Projects/HBN'
        if modality == 'EEG':
            s3_prefix_midfix='/'.join([s3_prefix,modality])
            sub_prefix=''
        if modality == 'MRI':
            s3_prefix_midfix='/'.join([s3_prefix,modality,'Site-' + site])
            sub_prefix='sub-'

        s3_pheno_path = '/'.join([s3_prefix_midfix,'participants.tsv'])
        print(s3_pheno_path)

        # If output path doesn't exist, create it
        if not os.path.exists(out_dir):
            print 'Could not find %s, creating now...' % out_dir
            os.makedirs(out_dir)

        # Load the phenotype file from S3
        s3_pheno_file = urllib.urlopen(s3_pheno_path)
        pheno_list = s3_pheno_file.readlines()
        pheno_list=map(lambda x: str.replace(x, '"', ''), pheno_list)

        # Get header indices
        header = pheno_list[0].strip().split(',')
        try:
            id_idx = header.index('participant_id')
            release_num_idx = header.index('release_number')

        except Exception as exc:
            err_msg = 'Unable to extract header information from the pheno file: %s'\
                      '\nHeader should have pheno info: %s\nError: %s'\
                      % (s3_pheno_path, str(header), exc)
            raise Exception(err_msg)

        # Go through pheno file and build download paths
        print 'Collecting images of interest...'
        s3_paths = []


        if sublist_path:
            sublist_tmp=pd.read_csv(sublist_path,header=None,names=["participant_ID"])
            if sublist_tmp.shape[0]==1 and sublist_tmp.shape[1] > 1:
                sublist_tmp=sublist_tmp.T
            if 'NDAR' not in sublist_tmp.iloc[0,0]:
                sublist_tmp=sublist_tmp.iloc[1:]
            for Sub_id in sublist_tmp['participant_ID']:
                if dataformat == 'mat':
                    filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '.' + dataformat
                    s3_path = '/'.join([s3_prefix_midfix, filename]) 
                    if urllib.urlopen(s3_path).code == 200:
                        print 'Adding %s to download queue...' % s3_path
                        s3_paths.append(s3_path)   
                if dataformat == 'csv':
                    filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '_data.' + dataformat
                    s3_path = '/'.join([s3_prefix_midfix, filename]) 
                    if urllib.urlopen(s3_path).code == 200:
                        print 'Adding %s to download queue...' % s3_path
                        s3_paths.append(s3_path)  
                    filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '_event.' + dataformat
                    s3_path = '/'.join([s3_prefix_midfix, filename]) 
                    if urllib.urlopen(s3_path).code == 200:
                        print 'Adding %s to download queue...' % s3_path
                        s3_paths.append(s3_path)  

        else:

            for pheno_row in pheno_list[1:]:

                # Comma separate the row
                cs_row = pheno_row.strip().split(',')

                try:
                    # See if it was preprocessed
                    Sub_id = cs_row[id_idx].strip('sub-')
                    # Read in participant info
                    Sub_release_num = cs_row[release_num_idx]
                except Exception as exc:
                    err_msg = 'Error extracting info from phenotypic file, skipping...'
                    print err_msg
                    continue
                # If the filename isn't specified, skip
                if release_num == 'All':
                    # filename=sub_prefix+Sub_id + '.tar.gz'
                    if dataformat == 'mat':
                        filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '.' + dataformat
                        s3_path = '/'.join([s3_prefix_midfix, filename]) 
                        if urllib.urlopen(s3_path).code == 200:
                            print 'Adding %s to download queue...' % s3_path
                            s3_paths.append(s3_path)   
                    if dataformat == 'csv':
                        filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '_data.' + dataformat
                        s3_path = '/'.join([s3_prefix_midfix, filename]) 
                        if urllib.urlopen(s3_path).code == 200:
                            print 'Adding %s to download queue...' % s3_path
                            s3_paths.append(s3_path)  
                        filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '_event.' + dataformat
                        s3_path = '/'.join([s3_prefix_midfix, filename]) 
                        if urllib.urlopen(s3_path).code == 200:
                            print 'Adding %s to download queue...' % s3_path
                            s3_paths.append(s3_path)  

                elif Sub_release_num == release_num:
                    if dataformat == 'mat':
                        filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '.' + dataformat
                        s3_path = '/'.join([s3_prefix_midfix, filename]) 
                        if urllib.urlopen(s3_path).code == 200:
                            print 'Adding %s to download queue...' % s3_path
                            s3_paths.append(s3_path)   
                    if dataformat == 'csv':
                        filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '_data.' + dataformat
                        s3_path = '/'.join([s3_prefix_midfix, filename]) 
                        if urllib.urlopen(s3_path).code == 200:
                            print 'Adding %s to download queue...' % s3_path
                            s3_paths.append(s3_path)  
                        filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '_event.' + dataformat
                        s3_path = '/'.join([s3_prefix_midfix, filename]) 
                        if urllib.urlopen(s3_path).code == 200:
                            print 'Adding %s to download queue...' % s3_path
                            s3_paths.append(s3_path)  

        # And download the items
        total_num_files = len(s3_paths)
        for path_idx, s3_path in enumerate(s3_paths):
            rel_path = s3_path.lstrip(s3_prefix)
            download_file = os.path.join(out_dir, rel_path)
            download_dir = os.path.dirname(download_file)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            try:
                if not os.path.exists(download_file):
                    print 'Retrieving: %s' % download_file
                    urllib.urlretrieve(s3_path, download_file)
                    print '%.3f%% percent complete' % \
                          (100*(float(path_idx+1)/total_num_files))
                else:
                    print 'File %s already exists, skipping...' % download_file
            except Exception as exc:
                print 'There was a problem downloading %s.\n'\
                      'Check input arguments and try again.' % s3_path

    # Print all done
    print 'Done!'


# Make module executable
if __name__ == '__main__':

    # Import packages
    import argparse
    import os
    import sys

    # Init arparser
    parser = argparse.ArgumentParser(description=__doc__)

    # Required arguments
    parser.add_argument('-m', '--modality', nargs=1, required=True, type=str,
                        help='Modality of interest (e.g. \'EEG or MRI\')')

    parser.add_argument('-o', '--out_dir', nargs=1, required=True, type=str,
                        help='Path to local folder to download files to')
    parser.add_argument('-s', '--site', nargs=1, required=True, type=str,
                        help='Colleciton Site '\
                             '(e.g. \'SI, RU, CBIC, All\'')

    parser.add_argument('-p', '--paradigm', nargs=1, required=True, type=str,
                    help='paradigm to download '\
                         '(e.g. \'RestingState, SAIIT_2AFC_Block1, SAIIT_2AFC_Block2, SAIIT_2AFC_Block3, SurroundSupp_Block1, SurroundSupp_Block2, Video1, Video2, Video3, WISC_ProcSpeed, vis_learn\'')
    parser.add_argument('-rp', '--raw_preprocessed', nargs=1, required=True, type=str,
                    help='raw,preprocessed?'\
                         '(e.g. \'raw or preprocessed\'')

    parser.add_argument('-f', '--dataformat', nargs=1, required=True, type=str,
                help='dataformat'\
                     '(e.g. \'csv or mat\'')

    # Optional arguments
    parser.add_argument('-r', '--release_num', nargs=1, required=False, type=str,
                        help='Release Number '\
                             '(e.g. \'R1, R2, R3, All\')')

    parser.add_argument('-sub', '--subject_list', nargs=1, required=False, type=str,
                        help='Subject List '\
                             '(e.g. \'Full path of a csv file or just without this option to download all subjects\')')

    



    # Parse and gather arguments
    args = parser.parse_args()


    # Init variables
    modality = args.modality[0]
    out_dir = os.path.abspath(args.out_dir[0])
    site = args.site[0]
    paradigm=args.paradigm[0]
    raw_preprocessed=args.raw_preprocessed[0]
    dataformat=args.dataformat[0]


    # Try and init optional arguments
    try:
        release_num = args.release_num[0]
        print 'Extract data from release'+release_num+'...' 
    except TypeError as exc:
        release_num = 'All'
        print 'Extract data from all releases'

    try:
        sublist_path = args.subject_list[0]
        print 'Extract data from subject list '+sublist_path+'...' 
    except TypeError as exc:
        sublist_path = None
        print 'Extract data from all subject'


    # Call the collect and download routine
    collect_and_download(modality, release_num, site, paradigm, dataformat, raw_preprocessed, out_dir,sublist_path)

