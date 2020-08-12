#!/bin/sh

if [[ -z $1 || -z $2 || -z $3 ]]; then
  printf "usage: ./create_demultiplex.sh in out\n"
  exit 1
fi

INPUT_DIR=$1
OUTPUT_DIR=$2
SAMPLE_SHEET=$3

CMD="/opt/edico/bin/dragen --bcl-conversion-only true \\
  --bcl-input-directory ${INPUT_DIR} \\
  --output-directory ${OUTPUT_DIR} \\
  --sample-sheet ${SAMPLE_SHEET}"

echo "Running command: ${CMD}"

JOB_NAME=$(basename $1)
bsub -J $JOB_NAME -o ${JOB_NAME}.out -e ${JOB_NAME}.err -n48 -q dragen "${CMD}"


