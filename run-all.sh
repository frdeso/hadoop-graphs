set -x
RESULTS_PATH=$1
SUMMARY=${RESULTS_PATH}summary-1.csv
STARTTIME=${RESULTS_PATH}starttime-1.csv

TASKSDURATION=()
TASKSDURATION+=("${RESULTS_PATH}tasks_duration_job1-1.log")
#TASKSDURATION+=("${RESULTS_PATH}tasks_duration_job1-2.log")

python3 create-rectangle2.py ${TASKSDURATION[@]} > rect.gp
gnuplot -e "data='$SUMMARY'" -e "startTime='$STARTTIME'" -e "name='$RESULTS_PATH'"  report.gp
