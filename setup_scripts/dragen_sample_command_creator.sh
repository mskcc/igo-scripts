# mv: cannot stat ‘/igo/work/FASTQ/MICHELLE_0248_BHG7HVDSXY__HWG/Project_09443_BD/065IO_T_IGO_09443_BD_7*.fastq.gz’: No such file or directory

RUN_DIR=/igo/work/FASTQ/MICHELLE_0248_BHG7HVDSXY__HWG

PROJECT_DIRS=$(find ${RUN_DIR} -type d -name "Project_*")

for DIR in $PROJECT_DIRS; do
  FASTQ_FILES=$(find ${DIR} -maxdepth 1 -type f -name "*.fastq.gz" -exec basename {} \;)
  for FASTQ in ${FASTQ_FILES}; do
    RGSM=$(grep "${FASTQ}" ${RUN_DIR}/Reports/fastq_list.csv | cut -d',' -f2 | sort | uniq)
    echo "Found: ${RGSM}"
    SAMPLE_DIR=$DIR/$RGSM
    mkdir -p $SAMPLE_DIR
    mv $DIR/$RGSM*.fastq.gz $SAMPLE_DIR
    echo "Moved: ${RGSM}"
  done
done
