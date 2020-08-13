#!/bin/sh

# TODO
if [[ -z $1 || -z $2 ]]; then
  echo "usage: ./send_wgs.sh RUN_DIR REF_DIR"
  exit 1
fi

RUN_DIR=$1
FASTQ_LIST_CSV=${RUN_DIR}/Reports/fastq_list.csv
REF_DIR=$2

RUN=$(basename $RUN_DIR)  #  $(echo $FASTQ_LIST_CSV | cut -d'/' -f4)

printf "Creating Commands for Run: ${RUN}\n"

OUT_DIR=./sample_scripts

mkdir -p ${OUT_DIR}

PROJECT_DIRS=$(find $RUN_DIR -maxdepth 1 -type d -name "Project_*")

for PROJECT_DIR in $PROJECT_DIRS; do
  PROJECT=$(basename $PROJECT_DIR)
  echo "Creating $PROJECT scripts"
  
  RGSMs=$(tail -n +2 ${FASTQ_LIST_CSV} | grep "$(basename ${PROJECT})" | cut -d',' -f2 | sort | uniq  )
  echo $RGSMs
  for sample in $RGSMs; do
    JOB_NAME=DRGN__${PROJECT}__${sample}
    RESULTS_DIR=/igo/stats/DRAGEN/${RUN}/${PROJECT}/${sample}
    printf "bsub -n48 -q dragen -J $JOB_NAME -o $JOB_NAME.out -e $JOB_NAME.err \\
      \"mkdir -p $RESULTS_DIR && \\ 
      /opt/edico/bin/dragen --ref-dir ${REF_DIR} \\
      --fastq-list ${FASTQ_LIST_CSV} \\
      --fastq-list-sample-id ${sample} \\
      --intermediate-results-dir /staging/temp \\
      --output-directory $RESULTS_DIR \\
      --output-file-prefix ${PROJECT}__${sample}\"
    " > ${OUT_DIR}/${JOB_NAME}.sh
  done
done
