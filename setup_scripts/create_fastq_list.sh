if [[ -z "$1" ]]; then
  echo "usage: ./create_fastq_list.sh path/to/fastq_list.csv"
fi

FASTQ_LIST=$1

samples=$(tail -n +2 $FASTQ_LIST)

#######################################
# Gets valid path for sample  
# Globals:
#   FASTQ_LIST - dragen fastq_list.csv
# Arguments:
#   fastq - absolute path to FASTQ
#######################################
function create_path() {
  fastq=$1
  path=$(dirname $fastq)
  samp=$(basename $fastq)
  samp_dir=$(grep "${samp}"  ${FASTQ_LIST} | cut -d',' -f2 | sort | uniq)
  if [[ -z $(echo "${samp_dir}" | grep -E "^Sample_*") ]]; then
    samp_dir=Sample_${samp_dir}
  fi

  valid_path=$path/$samp_dir/$samp
  if [[ ! -f $valid_path ]]; then
    echo "Invalid path: $valid_path"
    exit 1
  fi
  echo $valid_path
}

NEW_CSV="./fastq_list_formatted.csv"
head -1 $FASTQ_LIST > $NEW_CSV
for fastq_line in $samples; do
  unchanged=$(echo $fastq_line | cut -d ',' -f1,2,3,4)
  r1=$(echo $fastq_line | cut -d',' -f5)
  r2=$(echo $fastq_line | cut -d',' -f6) 
  
  r1_formatted=$(create_path $r1)
  r2_formatted=$(create_path $r2) 
  echo "${unchanged},${r1_formatted},${r2_formatted}" >> $NEW_CSV
done

