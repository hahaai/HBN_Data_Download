# download_HBN_data_files_Windows.py
#
# Author: Lei AI, 2018

'''
This script downloads data from the HBN data release and stores the files in a local
directory; users specify modality (EEG), Site, and release number.
Usage:
    python download_HBN_preproc.py -m <data modality> -s <site>
                                     -r <release number> -o <out_dir>
                                     -s <colleciotn site> -p <paradigm names>
                                     -f <file format> -rp <raw or preprocessed>

Example:
python download_HBN_EEG_files_Windows.py -m EEG -s All -r All -o HBN_data -p Video1 -f mat -rp raw
'''


# Main collect and download function
def collect_and_download(modality, release_num, site, paradigm, format, raw_preprocessed, out_dir):

    '''
    Function to collect and download images from the ABIDE preprocessed
    directory on FCP-INDI's S3 bucket
    Parameters
    ----------
    -m modality : string
        EEG or MRI
    -r release_num : string
        1, 2,  3, All
    -s site : string
        SI, RU, CBIC, All
    -p paradigm : string
        RestingState, SAIIT_2AFC_Block1, SAIIT_2AFC_Block2, SAIIT_2AFC_Block3, SurroundSupp_Block1, SurroundSupp_Block2, Video1, Video2, Video3, WISC_ProcSpeed, vis_learn
    -f dataformat : string
        mat or csv
    -rp raw_preprocessed : string
        raw or preprocessed
    out_dir : string
        filepath to a local directory to save files to
    Returns
    -------
    None
        this function does not return a value; it downloads data from
        S3 to a local directory

    '''
    
    # Import packages
    import os
    import urllib.request

    if modality == 'MRI' and site == 'All' or site == 'all' or site == 'ALL':
        site_list=['SI','RU','CBIC']
    else:
        site_list=[site]

    for site in site_list:
        # Init variables
        s3_prefix = 'https://s3.amazonaws.com/fcp-indi/data/Projects/HBN'
        print(modality)
        if modality == 'EEG':
            print('ttttt')
            s3_prefix_midfix='/'.join([s3_prefix,modality])
            sub_prefix=''
        if modality == 'MRI':
            s3_prefix_midfix='/'.join([s3_prefix,modality,'Site-' + site])
            sub_prefix='sub-'

        s3_pheno_path = '/'.join([s3_prefix_midfix,'participants.tsv'])
        print(s3_pheno_path)

        # If output path doesn't exist, create it
        if not os.path.exists(out_dir):
            print ('Could not find %s, creating now...' % out_dir)
            os.makedirs(out_dir)

        # Load the phenotype file from S3
        s3_pheno_file = urllib.request.urlopen(s3_pheno_path)
        pheno_list = s3_pheno_file.readlines()
        print(pheno_list[0])
        #pheno_list=map(lambda x: str.replace(x, '"', ''), pheno_list)

        # Get header indices
        header = pheno_list[0].decode().strip().replace('"','').split(',')
        #header=header[0][:].replace('"','')
        try:
            id_idx = header.index('participant_id')
            release_num_idx = header.index('release_number')

        except Exception as exc:
            err_msg = 'Unable to extract header information from the pheno file: %s'\
                      '\nHeader should have pheno info: %s\nError: %s'\
                      % (s3_pheno_path, str(header), exc)
            raise Exception(err_msg)

        # Go through pheno file and build download paths
        print ('Collecting images of interest...')
        s3_paths = []
        for pheno_row in pheno_list[1:]:

            # Comma separate the row
            cs_row = pheno_row.decode().strip().split(',')
            #cs_row=cs_row[:].replace('"','')
            try:
                # See if it was preprocessed
                Sub_id = cs_row[id_idx].strip('sub-').replace('"','')
                # Read in participant info
                Sub_release_num = cs_row[release_num_idx]
            except Exception as exc:
                err_msg = 'Error extracting info from phenotypic file, skipping...'
                print (err_msg)
                continue
            # If the filename isn't specified, skip
            if release_num == 'All':
                # filename=sub_prefix+Sub_id + '.tar.gz'
                filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '.' + dataformat
                s3_path = '/'.join([s3_prefix_midfix, filename]) 
                try:
                    urllib.request.urlopen(s3_path).code
                    print ('Adding %s to download queue...' % s3_path)
                    s3_paths.append(s3_path)
                except urllib.request.HTTPError as err:
                    print('Not Existing')
            elif Sub_release_num == release_num:
                filename=sub_prefix+Sub_id + '/EEG/' + raw_preprocessed + '/' + dataformat + '_format/' + paradigm + '.' + dataformat
                s3_path = '/'.join([s3_prefix_midfix, filename]) 
                try:
                    urllib.request.urlopen(s3_path).code
                    print ('Adding %s to download queue...' % s3_path)
                    s3_paths.append(s3_path)
                except urllib.request.HTTPError as err:
                    print('Not Existing')

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
                    print ('Retrieving: %s' % download_file)
                    urllib.request.urlretrieve(s3_path, download_file)
                    print ('%.3f%% percent complete')
                else:
                    print ('File %s already exists, skipping...' % download_file)
            except Exception as exc:
                print ('There was a problem downloading %s.\n')

    # Print all done
    print ('Done!')


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
                         '(e.g. \'RestingState, Video1, Video2,...., All\'')
    parser.add_argument('-rp', '--raw_preprocessed', nargs=1, required=True, type=str,
                    help='raw,preprocessed?'\
                         '(e.g. \'True or False\'')

    parser.add_argument('-f', '--dataformat', nargs=1, required=True, type=str,
                help='dataformat'\
                     '(e.g. \'csv or mat\'')

    # Optional arguments
    parser.add_argument('-r', '--release_num', nargs=1, required=False, type=str,
                        help='Release Number '\
                             '(e.g. \'R1, R2, R3, All\')')
    



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
        print ('Extract data from release'+release_num+'...' )
    except TypeError as exc:
        release_num = 'All'
        print ('Extract data from all releases')


    # Call the collect and download routine
    collect_and_download(modality, release_num, site, paradigm, dataformat, raw_preprocessed, out_dir)
