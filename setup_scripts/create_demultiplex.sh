#!/bin/sh

if [[ -z $1 || -z $2 || -z $3 ]]; then
  printf "usage: ./create_demultiplex.sh in out sample_sheet\n"
  exit 1
fi

INPUT_DIR=$1
OUTPUT_DIR=$2
SAMPLE_SHEET=$3

CMD="/opt/edico/bin/dragen --bcl-conversion-only true \
  --bcl-input-directory ${INPUT_DIR} \
  --output-directory ${OUTPUT_DIR} \
  --bcl-sampleproject-subdirectories true \
  --sample-sheet ${SAMPLE_SHEET}"

echo "Writing command: ${CMD}"
JOB_NAME=$(basename $3 | cut -d'.' -f1)

echo "bsub -J $JOB_NAME -o ${JOB_NAME}.out -e ${JOB_NAME}.err -n48 -q dragen \"${CMD}\"" >  ${JOB_NAME}.sh


