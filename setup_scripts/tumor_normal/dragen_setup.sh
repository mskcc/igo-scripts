#!/bin/bash 

if [[ -z "$1" || -z "$2" ]]; then
   echo "Please specify csv & command config"
   exit
fi

CSV_CONFIG=$1
COMMAND_CONFIG=$2

COMMAND_DIR="./commands"
mkdir -p $COMMAND_DIR

while read -r -a argArray; do
   if [ ${#argArray[@]} -eq 2 ]; then
      FASTQ_PATH="${argArray[0]}"
      SAMPLE="${argArray[1]}"
      /home/streidd/igo-scripts/setup_scripts/filtered_pairs.sh $FASTQ_PATH $SAMPLE
   fi
done < $CSV_CONFIG

echo ""

while read -r -a argArray; do
   if [ ${#argArray[@]} -eq 3 ]; then
      PROJECT="${argArray[0]}"
      TUMOR_ID="${argArray[1]}"
      NORMAL_ID="${argArray[2]}"
      SCRIPT=${COMMAND_DIR}/${PROJECT}.sh
      OUTPUT_DIR=/staging/${PROJECT}

      echo "Creating command for ${PROJECT}"
 
      echo "/opt/edico/bin/dragen \\" > $SCRIPT
      echo "   --ref-dir /staging/GRCh37 \\" >> $SCRIPT
      echo "   --enable-duplicate-marking true \\" >> $SCRIPT
      echo "   --enable-variant-caller true \\" >> $SCRIPT
      echo "   --fastq-list /staging/csv/${NORMAL_ID}.csv \\" >> $SCRIPT
      echo "   --fastq-list-sample-id ${NORMAL_ID} \\" >> $SCRIPT
      echo "   --tumor-fastq-list /staging/csv/${TUMOR_ID}.csv \\" >> $SCRIPT
      echo "   --tumor-fastq-list-sample-id ${TUMOR_ID}  \\" >> $SCRIPT
      echo "   --output-directory ${OUTPUT_DIR} \\" >> $SCRIPT
      echo "   --output-file-prefix ${PROJECT} &&" >> $SCRIPT
      echo "(aws s3 sync ${OUTPUT_DIR} s3://dragen.msk/dragen_runs/${PROJECT} &)" >> $SCRIPT
   fi
done < $COMMAND_CONFIG

echo "DONE."
echo "Copy ./csv to /staging/csv"
echo "Create these directories"

while read -r -a argArray; do
   if [ ${#argArray[@]} -eq 3 ]; then
      PROJECT="${argArray[0]}"
      echo "/staging/${PROJECT}"
   fi
done < $COMMAND_CONFIG

echo $DONE
