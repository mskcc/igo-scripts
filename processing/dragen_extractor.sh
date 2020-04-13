# Run this in the output-directory of the dragen run

DRAGEN_MAPPING_FILE="mapping_metrics.csv"
DRAGEN_OVERALL_COV_FILE="overall_mean_cov*.csv"
DRAGEN_COV_METRICS_FILE="coverage_metrics*.csv"

# "MAPPING/ALIGNING SUMMARY,,Q30 bases," 
# "Number of unique reads (excl. duplicate marked reads),"
DRAGEN_MAPPING_FIELDS=(
   "Properly paired reads"
   "Not properly paired reads,"
   "Unmapped reads,"
   "Number of duplicate marked reads,"
   "Total input reads,"
   "Total bases,"
)
# "Average alignment coverage over"
DRAGEN_OVERALL_COV_FIELDS=(
   "Average alignment coverage over target_bed"
)

# "Aligned reads"
# "Aligned bases"
DRAGEN_COV_METRICS_FIELDS=(
   "Aligned reads in target region"
   "Aligned bases in target region"
   "Average alignment coverage over target region"
   "1x: inf"
   "10x: inf"
   "20x: inf"
   "50x: inf"
   "100x: inf"
)

# WGS
all_file_types=($DRAGEN_MAPPING_FILE $DRAGEN_OVERALL_COV_FILE $DRAGEN_COV_METRICS_FILE)
for file_type in ${all_file_types[@]}
do
   # If not WES, remove 'grep -v "wgs_coverage_metrics"'
   target_files=$(find . -type f -name "*${file_type}" | grep -v "wgs_coverage_metrics")
   for file in ${target_files[@]}
   do
      for field in "${DRAGEN_MAPPING_FIELDS[@]}"; do
         grep -i "$field" $file | grep -v "PER RG"
      done
      # echo $file # tumor/normal are kept in seperate files
      for field in "${DRAGEN_OVERALL_COV_FIELDS[@]}"; do
         grep "$field" $file
      done
      for field in "${DRAGEN_COV_METRICS_FIELDS[@]}"; do
         grep "$field" $file
      done
   done
done

