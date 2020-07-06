#!/bin/bash

if [[ -z "$1"  ||  -z "$2" ]]
  then
    printf "Please provide a fastq directory and sample. See below,\n\t./create_dragen_fastq_list.sh /ifs/input/GCL/hiseq/FASTQ/JAX_0430_BHGLHLBBXY/Project_10807/ 10807 wes\n"
  exit 1
fi


PROJECT_DIR=$1
SAMPLE=$2
OUTPUT_CSV=./csv/$SAMPLE.csv

mkdir -p ./csv

DRAGEN_CSV="/staging/csv/${OUTPUT_CSV}"

# load config
. /home/streidd/igo-scripts/setup_scripts/pipeline.config

# CREATE CSV
if [ ! -f "$OUTPUT_CSV" ]; then
   printf "\nCreating ${OUTPUT_CSV}\n"
   headers="RGID,RGSM,RGLB,Lane,Read1File,Read2File"
   echo $headers > $OUTPUT_CSV
fi

if [ ! -d ${PROJECT_DIR} ]; then
   echo "${PROJECT_DIR} does not exist"
   exit 1
fi

echo "Searching ${PROJECT_DIR} directory"

sample_sheets=$(find $PROJECT_DIR -type f -name "SampleSheet.csv")
for sample_sheet in $sample_sheets
do
   dir=$(dirname $sample_sheet)
   fastqs=$(find $dir -type f -name "*.fastq.gz")
 
   num_fastqs=$(echo $fastqs | wc -w)
   if [[ "$num_fastqs" != "2" ]] ; then
      echo "Invalid FASTQ number";
      exit;
   fi

   fastq1_path=$(echo $fastqs | tr -s ' ' | cut -d' ' -f 1)
   fastq2_path=$(echo $fastqs | tr -s ' ' | cut -d' ' -f 2)
 
   s3_PATH_1=$(echo ${fastq1_path/\/ifs\/archive\/GCL\/hiseq\/FASTQ\///})
   s3_PATH_2=$(echo ${fastq2_path/\/ifs\/archive\/GCL\/hiseq\/FASTQ\///})
   {
      read
      while IFS=, read -r FCID Lane SampleID SampleRef Index Description Control Recipe Operator SampleProject
      do
         line="$FCID.$SampleID.$Lane,$SampleID,$SampleID,$Lane,s3://dragen.msk${s3_PATH_1},s3://dragen.msk${s3_PATH_2}"
         echo $line >> $OUTPUT_CSV
      done
   } < $sample_sheet   
done
