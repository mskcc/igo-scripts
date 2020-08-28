# mv: cannot stat ‘/igo/work/FASTQ/MICHELLE_0248_BHG7HVDSXY__HWG/Project_09443_BD/065IO_T_IGO_09443_BD_7*.fastq.gz’: No such file or directory

if [[ -z "$1" ]]; then
  echo "usage: ./dragen_sample_command_creator.sh {RUN_DIR}"
  printf "e.g.\n\t./dragen_sample_command_creator.sh /igo/work/FASTQ/MICHELLE_0248_BHG7HVDSXY__HWG\n"
fi

RUN_DIR=$1

PROJECT_DIRS=$(find ${RUN_DIR} -type d -name "Project_*")
for DIR in $PROJECT_DIRS; do
  FASTQ_FILES=$(find ${DIR} -maxdepth 1 -type f -name "*.fastq.gz" -exec basename {} \;)
  for FASTQ in ${FASTQ_FILES}; do
    # Some FASTQs may have already been moved
    if [[ -f "${DIR}/${FASTQ}" ]]; then
      RGSM=$(grep "${FASTQ}" ${RUN_DIR}/Reports/fastq_list.csv | cut -d',' -f2 | sort | uniq)
      echo "Found: ${RGSM}"
      # Sample directory NEEDS to be pre-fixed with "Sample_"
      if [[ -z $(echo "${RGSM}" | grep -E "^Sample_*") ]]; then
        SAMPLE_DIR=$DIR/Sample_$RGSM
      else
        SAMPLE_DIR=$DIR/$RGSM
      fi
      mkdir -p $SAMPLE_DIR
      mv $DIR/$RGSM*.fastq.gz $SAMPLE_DIR
      echo "Moved: ${RGSM} to ${SAMPLE_DIR}"
    else
      echo "Already Moved: ${FASTQ}"
    fi
  done
done
