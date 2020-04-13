# Run this in the output-directory of the dragen run

DRAGEN_MAPPING_FILE="mapping_metrics.csv"
DRAGEN_OVERALL_COV_FILE="overall_mean_cov.csv"
DRAGEN_COV_METRICS_FILE="coverage_metrics.csv"

DRAGEN_MAPPING_FIELDS=(
   "Total input reads,"
   "Total bases,"
   "Number of unique reads (excl. duplicate marked reads),"
   "Number of unique reads (excl. duplicate marked reads),"
   "Total bases,"
   "MAPPING/ALIGNING SUMMARY,,Q30 bases,"
)
DRAGEN_OVERALL_COV_FIELDS=(
   "Average alignment coverage over"
)
DRAGEN_COV_METRICS_FIELDS=(
   "1x: inf"
   "10x: inf"
   "20x: inf"
   "50x: inf"
   "100x: inf"
)

all_file_types=($DRAGEN_MAPPING_FILE $DRAGEN_OVERALL_COV_FILE $DRAGEN_COV_METRICS_FILE)
for file_type in ${all_file_types[@]}
do
   target_files=$(find . -type f -name "*${file_type}")
   for file in ${target_files[@]}
   do
      for field in "${DRAGEN_MAPPING_FIELDS[@]}"; do
         grep -i "$field" $file
      done
      for field in "${DRAGEN_OVERALL_COV_FIELDS[@]}"; do
         grep -i "$field" $file
      done
      for field in "${DRAGEN_COV_METRICS_FIELDS[@]}"; do
         grep "$field" $file
      done
   done
done

