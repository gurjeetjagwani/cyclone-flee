#!/bin/bash
export PYTHONPATH="$(dirname "$PWD")"

# setting variables
NUM_INSTANCES=3
cores=1

# INPUT_DATA_DIR="ssudan-mscale"
INPUT_DATA_DIR="ssudan-mscale-test"
RUN_PYTHON_FILE="run_mscale.py"

LOG_EXCHANGE_DATA="True"
COUPLING_TYPE="file"
WEATHER_COUPLING="False"

#-------------------------------------------------------
#             parse input arguments
#-------------------------------------------------------
# cores=${cores:-1}
while [ $# -gt 0 ]; do
  if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo -e "\nUsage:"
    echo -e "\t ./run_file_coupling.sh.sh < --cores N > < --NUM_INSTANCES M >\n"
    exit 1
  fi
  if [[ $1 == *"--"* ]]; then
      param="${1/--/}"
      if [ -n "${!param}" ]; then
        declare $param="$2"
      else
        echo -e "\nError !!! Input arg --$param is not valid\n" 
        echo -e "you can use -h or --help option to see the valid input arguments\n"
        exit 1
      fi
  fi
  shift
done

#-------------------------------------------------------
#             convert to lowercase
#-------------------------------------------------------
function covert_to_lowercase()
{
   echo $(echo "$1" | tr "[:upper:]" "[:lower:]")
}

LOG_EXCHANGE_DATA=$(covert_to_lowercase $LOG_EXCHANGE_DATA)
COUPLING_TYPE=$(covert_to_lowercase $COUPLING_TYPE)
WEATHER_COUPLING=$(covert_to_lowercase $WEATHER_COUPLING)


#-------------------------------------------------------
#             set run_command variable
#-------------------------------------------------------
function set_run_command()
{
  run_command=""  
  if [ "$cores" -gt "1" ];
  then
    run_command="mpirun -n $cores python3"
  else
    run_command="python3"
  fi
}

set_run_command


#-------------------------------------------------------
#             clean output directory
#-------------------------------------------------------


if [ $WEATHER_COUPLING = "true" ];
then
  rm -rf out/weather/$COUPLING_TYPE/*
  mkdir -p out/weather/$COUPLING_TYPE/coupled
  mkdir -p out/weather/$COUPLING_TYPE/macro
  mkdir -p out/weather/$COUPLING_TYPE/micro
  mkdir -p out/weather/$COUPLING_TYPE/log_exchange_data
  mkdir -p out/weather/$COUPLING_TYPE/plot_exchange_data
else
  rm -rf out/$COUPLING_TYPE/*
  mkdir -p out/$COUPLING_TYPE/coupled
  mkdir -p out/$COUPLING_TYPE/macro
  mkdir -p out/$COUPLING_TYPE/micro
  mkdir -p out/$COUPLING_TYPE/log_exchange_data
  mkdir -p out/$COUPLING_TYPE/plot_exchange_data
fi


#-------------------------------------------------------
#             return common input arguments
#-------------------------------------------------------
function ret_common_args()
{
  local common_args="--data_dir=$INPUT_DATA_DIR \
    --log_exchange_data $LOG_EXCHANGE_DATA \
    --instance_index $i \
    --coupling_type $COUPLING_TYPE \
    --num_instances $NUM_INSTANCES \
    --weather_coupling $WEATHER_COUPLING"
    echo $common_args
}


start_time="$(date -u +%s.%N)"


# index should be started from 0
for i in $(seq 0 $(($NUM_INSTANCES-1)))
do
  common_args="$(ret_common_args)"

  $run_command $RUN_PYTHON_FILE  --submodel macro $common_args &
  $run_command $RUN_PYTHON_FILE  --submodel micro $common_args &
done

wait

end_time="$(date -u +%s.%N)"
elapsed="$(bc <<<"$end_time-$start_time")"

#-------------------------------------------------------
#             reporting
#-------------------------------------------------------
#printf '=%.0s' {1..70}
for i in {1..70}; do echo -n =; done
echo -e "\nExecuted commands :"


for i in $(seq 0 $(($NUM_INSTANCES-1)))
do
  common_args="--data_dir=$INPUT_DATA_DIR \
  --instance_index $i \
  --coupling_type $COUPLING_TYPE \
  --num_instances $NUM_INSTANCES \
  --weather_coupling $WEATHER_COUPLING"

  echo -e "\t $run_command $RUN_PYTHON_FILE --submodel macro $common_args"  
  echo -e "\t $run_command $RUN_PYTHON_FILE --submodel micro $common_args"
done  


echo -e "\n\nTotal Executing Time = $elapsed seconds\n" 