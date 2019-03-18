#!/bin/bash

# This will download the HBN MRI data.
# usuage: bash download_HBN_MRI_files.sh /Users/lei.ai/Downloads/HBN_MRI 'T2w'
# Author: Lei Ai, CMI 2018 Aug
# Update March 2019, add more options.

#===============================================================================
#
#          FILE:  MRI_S3_downloader.sh
#
#         USAGE:  ./bash MRI_S3_downloader.sh ~/Downloads/HBM_MRI 'dwi' 'All' 'sublist.txt'
#
#   DESCRIPTION: 
#
#       OPTIONS:  Dataout path, 
#                 Data type to download: T1w, T2w, MT-on, MT-off, dwi, fmap, peer, rest, movieDM, movieTP
#                 Site to download: SI, RU, CBIC or All. * All will download the data from all sites
#                 Subject list path to download: optional. A text file with subject names (NDAR***) to download  
#  REQUIREMENTS:  AWS CLI:https://aws.amazon.com/cli/
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  Lei Ai lei.ai@childmind.org
#       COMPANY:  CMI
#       VERSION:  
#       CREATED:  Augest 2018
#      REVISION:  March 2019
#===============================================================================



display_usage() { 
    echo -e "\nUsage: ./bash MRI_S3_downloader.sh ~/Downloads/HBM_MRI 'dwi' 'All' sublist.txt "
    echo -e "\nThe first three options (outputpath, type, site) are required, the fourth subject list option is optional. \n" 
} 

# if less than two arguments supplied, display usage 
if [  $# -le 2 ];then 
    display_usage
    exit 1
fi 



dataout=$1
downloadpattern=$2
site=$3
sublist=$4


# aws s3 cp s3://fcp-indi/data/Projects/HBN/MRI/Site-CBIC/sub-NDARAY461TZZ/anat/ /Users/lei.ai/Downloads/HBN_MRI  --exclude "*" --include "*_T2w*" --recursive

if [[ "$downloadpattern" == *"T2w"* ]] || [[ "$downloadpattern" == *"T1w"* ]] || [[ "$downloadpattern" == *"MT-on"* ]] || [[ "$downloadpattern" == *"MT-off"* ]];then
	mri_type='anat'
elif [[ "$downloadpattern" == *"dwi"* ]];then
	mri_type='dwi'
elif [[ "$downloadpattern" == *"fmap"* ]];then
	mri_type='fmap'
elif [[ "$downloadpattern" == *"peer"* ]] || [[ "$downloadpattern" == *"rest"* ]] || [[ "$downloadpattern" == *"movieDM"* ]] || [[ "$downloadpattern" == *"movieTP"* ]];then
    mri_type='func'
else
	echo "NOT the right download pattern. Please input the following: T1w, T2w, MT-on, MT-off, dwi, fmap, peer, rest, movieDM, movieTP"
	exit 1
fi


# if site to download is specified.

if [[ $site = 'All' ]];then
    echo 'Download from all sites'
    for site in $(aws s3 ls s3://fcp-indi/data/Projects/HBN/MRI/);do
        if [[ "$site" == *"Site-"* ]];then
            echo $site
            mkdir -p $dataout'/'$site

            if [[ -z $sublist ]];then 
                for sub in $(aws s3 ls s3://fcp-indi/data/Projects/HBN/MRI/$site);do
                    if [[ "$sub" == *"sub-"* ]];then
                        echo $sub
                        if [[ ! -z $(aws s3 ls s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/') ]];then 
                            aws s3 sync s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/' $dataout'/'$site$sub$mri_type  --exclude "*" --include "*${downloadpattern}*"
                        fi
                    fi
                done
            else
                if [[ ! -f $sublist ]];then
                    echo subject list file not exist.
                else   
                    for sub in $(cat $sublist);do
                        echo $sub
                        if [[ ${sub:0:4} != 'NDAR' ]];then
                            echo Subject ID format not correct, they should be NDAR****
                        else
                            sub='sub-'$sub'/'
                            if [[ ! -z $(aws s3 ls s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/') ]];then 
                                aws s3 sync s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/' $dataout'/'$site$sub$mri_type  --exclude "*" --include "*${downloadpattern}*"
                            fi
                        fi
                    done
                fi
                
            fi




        fi
    done
else
    #echo $site
    # check is site information input is correct
    if [[ $site != 'RU' ]] && [[ $site != 'CBIC' ]] && [[ $site != 'SI' ]];then
        echo Site information incorret, please input RU, CBIC, or SI. Or All to downlaod form all sites.
    else
        site='Site-'$site'/'
        mkdir -p $dataout'/'$site
        if [[ -z $sublist ]];then 
            for sub in $(aws s3 ls s3://fcp-indi/data/Projects/HBN/MRI/$site);do
                if [[ "$sub" == *"sub-"* ]];then
                    echo $sub
                    if [[ ! -z $(aws s3 ls s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/') ]];then 
                        aws s3 sync s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/' $dataout'/'$site$sub$mri_type  --exclude "*" --include "*${downloadpattern}*"
                    fi
                fi
            done
        else
            if [[ ! -f $sublist ]];then
                echo subject list file not exist.
            else   
                for sub in $(cat $sublist);do
                    echo Start downloading form $sublist
                    echo $sub
                    if [[ ${sub:0:4} != 'NDAR' ]];then
                        echo Subject ID format not correct, they should be NDAR****
                    else
                        sub='sub-'$sub'/'
                        if [[ ! -z $(aws s3 ls s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/') ]];then 
                            aws s3 sync s3://fcp-indi/data/Projects/HBN/MRI/$site$sub$mri_type'/' $dataout'/'$site$sub$mri_type  --exclude "*" --include "*${downloadpattern}*"
                        fi
                    fi
                done
            fi
            
        fi


    fi
fi


