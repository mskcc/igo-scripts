# Run this in the IGO project file

# FILE and FIELDS we care about
HS_METRICS_FILE="___hs.txt"
HS_METRICS_FIELDS=(
   TOTAL_READS
   PF_BASES
   PF_UNIQUE_READS
   PF_UQ_READS_ALIGNED
   PF_BASES_ALIGNED
   PF_UQ_BASES_ALIGNED
   MEAN_TARGET_COVERAGE
   PCT_TARGET_BASES_1X
   PCT_TARGET_BASES_10X
   PCT_TARGET_BASES_20X
   PCT_TARGET_BASES_50X
   PCT_TARGET_BASES_100X
)

hs_file=$(find . -type f -name "*${HS_METRICS_FILE}")
for file in $hs_file; do
   # ___hs.txt file is the tab-delimited output of picard
   # e.g. 
   #    ## METRICS CLASS...
   #    BAIT_SET BAIT_TERRITORY BAIT_DESIGN_EFFICIENCY...
   #    IDT_Exome_v1_FP_b37_baits 50843958 0.764658...
   columns=$(grep -A1 "## METRICS CLASS" $file | grep -v "## METRICS CLASS")
   values=$(grep -A2 "## METRICS CLASS" $file | grep -v "## METRICS CLASS" | grep -v "BAIT_SET")
   IFS=$'\t' read -r -a column_list <<< "$columns"	# Transform into list
   IFS=$'\t' read -r -a value_list <<< "$values"
   for i in "${!column_list[@]}"; do 
      col="${column_list[$i]}"
      val="${value_list[$i]}"
      # Only grab the FIELDS we care about
      for target_col in ${HS_METRICS_FIELDS[@]}; do
         if [ "$target_col" = "$col" ]; then
            echo "${col}: ${val}"
         fi
      done
   done
done
