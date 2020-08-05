#!/bin/bash

if [[ -z "$1"  ]]
  then
    printf "Please provide a project directory. See below,\n\t./create_dragen_csv.sh /ifs/input/GCL/hiseq/FASTQ/JAX_0430_BHGLHLBBXY/Project_10807\n"
  exit 1
fi

PROJECT_DIR=$1
PROJECT=$(basename $PROJECT_DIR)
OUTPUT_CSV=${PROJECT}.csv
DRAGEN_CSV="/staging/csv/${PROJECT}/${OUTPUT_CSV}"

# CSV-Reading
LANE_IDX=2
SAMP_IDX=3
FCID_IDX=1
OPRT_IDX=9

# read  -n 1 -p "Create CSV with name (y/n): " user_answer
user_answer="y"
if [[ "${user_answer}" != "y" ]]; then
  echo "Please give a valid Project directory"
  exit
fi


# CREATE CSV
headers="RGID,RGSM,RGLB,Lane,Read1File,Read2File"
echo $headers > $OUTPUT_CSV

sample_sheets=$(find $PROJECT_DIR -type f -name "SampleSheet.csv")
for sample_sheet in $sample_sheets; do
   dir=$(dirname $sample_sheet)
   echo "Searching ${dir} for FASTQ pairs"
   for line in $(tail -n +2 $sample_sheet); do
      LANE=$(echo $line | cut -d',' -f${LANE_IDX})
      SAMP=$(echo $line | cut -d',' -f${SAMP_IDX})
      RGID=$(echo $line | cut -d',' -f${FCID_IDX})
      OPRT=$(echo $line | cut -d',' -f${OPRT_IDX})

      # Get Illumina end-segments (have seen these go up to 14)
      for idx in {1..9}; do
         F1=$(find $dir -type f -name "${SAMP}*L00${LANE}_R1_00${idx}*.fastq.gz")
         F2=$(find $dir -type f -name "${SAMP}*L00${LANE}_R2_00${idx}*.fastq.gz")
         if [[ -z "${F1}" || -z "${F2}"  ]]; then
            printf "\tFound $( expr $idx - 1 ) fastq pairs in for $SAMP ${LANE}\n"
            break
         fi
         echo "$RGID,$SAMP,$OPRT,$LANE,$F1,$F2" >> $OUTPUT_CSV
      done
      for idx in {10..99}; do
         F1=$(find $dir -type f -name "${SAMP}*L00${LANE}_R1_0${idx}*.fastq.gz")
         F2=$(find $dir -type f -name "${SAMP}*L00${LANE}_R2_0${idx}*.fastq.gz")
         if [[ -z "${F1}" || -z "${F2}"  ]]; then
            printf "\tFound $( expr $idx - 1 ) fastq pairs in for $SAMP ${LANE}\n"
            break
         fi
         echo "$RGID,$SAMP,$OPRT,$LANE,$F1,$F2" >> $OUTPUT_CSV
      done
   done
done

expected_fastq=$(find $PROJECT_DIR -type f -name "*.fastq.gz" | wc -l)
csv_lines=$(cat ${OUTPUT_CSV} | wc -l)
actual_pairs=$( expr $csv_lines - 1 )
expected_pairs=$( expr $expected_fastq / 2 )

echo "Actual Pairs: ${actual_pairs}, Expected_pairs: ${expected_pairs}"
if [[ $expected_pairs -ne $actual_pairs ]]; then 
   echo "Warning: Unexpected number of FASTQ pairs"; 
else
   echo "CSV looks good!"
   echo "Next steps (On dragen) - Copy ${OUTPUT_CSV} to ${DRAGEN_CSV} on DRAGEN node"
fi

