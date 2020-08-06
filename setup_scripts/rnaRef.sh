#!/bin/bash

if [[ -z "$1"  ||  -z "$2" ]]; then
  printf "please specify an input fasta & output directory, e.g.
\t./sendRefJob.sh FASTA.fa /DRAGEN/OUT/DIR
\t./sendRefJob.sh /igo/work/nabors/genomes/GRCm38/Mus_musculus.GRCm38.dna.primary_assembly.fa /staging/ref/GRCm38_rna
"
  exit
fi

INPUT_FA=$1
OUT_DIR=$2
 
CMD="mkdir -p ${OUT_DIR} && /opt/edico/bin/dragen --build-hash-table true \\
  --ht-build-rna-hashtable true \\
  --enable-rna true \\
  --ht-reference ${INPUT_FA} \\
  --output-directory ${OUT_DIR}"

printf "Running command - ${CMD}\n"

JOB_NAME="RNA_REF:$(basename ${INPUT_FA})"

echo "Submitting ${JOB_NAME}"

bsub -J $JOB_NAME -o ${JOB_NAME}.out -e ${JOB_NAME}.err -n48 -q dragen "${CMD}"

