#!/bin/sh

if [[ -z $1 || -z $2 || -z $3 ]]; then
  printf "Please specify a project, annotation file, & reference - \"./create_dragen_sample_scripts.sh {PROJECT} {ANNOTATION_FILE} {REFERENCE}\"
./create_dragen_sample_scripts.sh Project_3539 /igo/work/nabors/genomes/GRCm38/Mus_musculus.GRCm38.99.gtf /staging/ref/GRCm38_rna
"
  exit 1
fi

PROJECT=$1
ANNOTATION_FILE=$2
REF_DIR=$3

printf "Creating Commands for Project: ${PROJECT}
\tAnnotation File: ${ANNOTATION_FILE}
\tReference File: ${REF_DIR}
"

FASTQ_LIST_CSV=${PROJECT}_fastq_list.csv

RGSMs=$(tail -n +2 ${FASTQ_LIST_CSV} | cut -d',' -f2 | sort | uniq  )
OUT_DIR=./sample_scripts

mkdir -p ${OUT_DIR}

for sample in $RGSMs; do
  JOB_NAME=DRGN__${PROJECT}__${sample}
  RESULTS_DIR=/igo/work/streidd/dragen/${PROJECT}/${sample}
  printf "bsub -n48 -q dragen -J $JOB_NAME -o $JOB_NAME.out -e $JOB_NAME.err \\
   \"mkdir -p $RESULTS_DIR && \\ 
   /opt/edico/bin/dragen --ref-dir ${REF_DIR} \\
   --enable-rna true \\
   --enable-rna-quantification true \\
   --annotation-file ${ANNOTATION_FILE} \\
   --fastq-list /igo/work/streidd/dragen/${PROJECT}/${FASTQ_LIST_CSV} \\
   --fastq-list-sample-id ${sample} \\
   --intermediate-results-dir /staging/temp \\
   --output-directory $RESULTS_DIR \\
   --output-file-prefix ${PROJECT}__${sample}\"
" > ${OUT_DIR}/${JOB_NAME}.sh
done
