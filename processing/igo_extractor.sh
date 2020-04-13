HS_METRICS_FILE="___hs.txt"

hs_file=$(find . -type f -name "*${HS_METRICS_FILE}")
for file in $hs_file; do
   columns=$(grep -A1 "## METRICS CLASS" $file | grep -v "## METRICS CLASS")
   values=$(grep -A2 "## METRICS CLASS" $file | grep -v "## METRICS CLASS" | grep -v "BAIT_SET")
   IFS=$'\t' read -r -a column_list <<< "$columns"
   IFS=$'\t' read -r -a value_list <<< "$values"
   for i in "${!column_list[@]}"; do 
      col="${column_list[$i]}"
      val="${value_list[$i]}"
      echo "${col}: ${val}"
   done
done
