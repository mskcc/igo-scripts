#!/bin/bash

if [[ -z "$1"  ||  -z "$2" || -z "$3" ]]
  then
    printf "Please provide a project directory and specify project/type. See below,\n\t./create_dragen_fastq_list.sh /ifs/input/GCL/hiseq/FASTQ/JAX_0430_BHGLHLBBXY/Project_10807/ 10807 wes\n"
  exit 1
fi


PROJECT_DIR=$1
PROJECT=$2
TYPE=$3
OUTPUT_CSV=$3_$2.csv
DRAGEN_CMD=$3_$2

DRAGEN_CSV="/staging/csv/${PROJECT}/${OUTPUT_CSV}"

# load config
. /home/streidd/igo-scripts/setup_scripts/pipeline.config

# Function to write commands to a bash script file
WRITE_CMD() {
   echo -e "nohup /opt/edico/bin/dragen --ref-dir /staging/GRCh37 \\ \n   --enable-duplicate-marking true \\" > $SAMPLE_CMD
   echo -e "   --vc-target-bed ${DRAGEN_BED} \\" >> $SAMPLE_CMD
   echo -e "   --fastq-list ${DRAGEN_CSV} \\" >> $SAMPLE_CMD
   echo -e "   --fastq-list-sample-id ${SampleID} \\" >> $SAMPLE_CMD
   echo -e "   --tumor-fastq-list /staging/csv/10807/wes_10807.csv \\" >> $SAMPLE_CMD
   echo -e "   --tumor-fastq-list-sample-id \\" >> $SAMPLE_CMD
   echo -e "   --output-directory /ephemeral/ \\" >> $SAMPLE_CMD
   echo -e "   --output-file-prefix ${PROJECT}_${SampleID} &" >> $SAMPLE_CMD
}

# CREATE CSV
headers="RGID,RGSM,RGLB,Lane,Read1File,Read2File"
echo $headers > $OUTPUT_CSV

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
  
   fastq1_file=$(basename $fastq1_path)
   fastq2_file=$(basename $fastq2_path)

   fastq1_parent=$(dirname $fastq1_path | rev | tr -s '/' | cut -d'/' -f1 | rev)
   fastq2_parent=$(dirname $fastq2_path | rev | tr -s '/' | cut -d'/' -f1 | rev)
 
   fastq1="${fastq1_parent}/${fastq1_file}"
   fastq2="${fastq2_parent}/${fastq2_file}"

   {
      read
      while IFS=, read -r FCID Lane SampleID SampleRef Index Description Control Recipe Operator SampleProject
      do 
         line="$FCID.$SampleID.$Lane,$SampleID,$SampleID,$Lane,s3://dragen.msk/$TYPE/$PROJECT/$fastq1,s3://dragen.msk/$TYPE/$PROJECT/$fastq2"
         
         # Create the commands
         SAMPLE_CMD="${DRAGEN_CMD}_${SampleID}.sh"
         WRITE_CMD

         echo $line >> $OUTPUT_CSV
      done
   } < $sample_sheet
done

echo "Next steps - On dragen"
echo "1) Copy ${OUTPUT_CSV} to ${DRAGEN_CSV} on dragen instance"
echo "2) For each run, copy the corresponding 'tumor-fastq-list-sample-id' into the command"
echo "3) Run all ${DRAGEN_CMD}_[SampleID].sh scripts on dragen instance"
