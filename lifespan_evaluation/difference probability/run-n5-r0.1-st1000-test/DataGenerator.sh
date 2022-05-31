#!/bin/bash 

if [ $# -lt 3 ]
then
    echo "usage: $0 <start> <end> <info>"
    exit
fi

SEED=11
N_NODES=5
CHANNEL_EXISTANCE_PROB=$(python -c "print(1)")
AVERAGE_CAPACITY=18000000
CAPACITY_STD=1800000
AVERAGE_PAYMENT_AMOUNT=1000
PAYMENT_AMOUNT_STD=0
MRATES_FILE="./Mrates.csv"
FEE_BASE=0
FEE_PROPORTIONAL=0
MIN_HTLC=100
TIMELOCK=140

SIMULATION_TIME=1000

SPARSE_COEF=$(python -c "print(1)")
AVERAGE_RATE=$(python -c "print(0.1)")
STD_RATE=$(python -c "print(0.1)")
MRATE_SKEW=4

CHANNEL_DATA_FOLDER="channels_data"




echo "----------------------------------start-genenation-------------------------------------"

result_dir="run-n$N_NODES-r$AVERAGE_RATE-st$SIMULATION_TIME-$3"

rm -r $result_dir
mkdir $result_dir
mkdir $result_dir/$CHANNEL_DATA_FOLDER

python3 mrates_generator.py $SEED $N_NODES $SPARSE_COEF $AVERAGE_RATE $STD_RATE $MRATE_SKEW

n_channels=$(python3 network_generator.py $SEED $N_NODES $CHANNEL_EXISTANCE_PROB $AVERAGE_CAPACITY $AVERAGE_PAYMENT_AMOUNT $MRATES_FILE $FEE_BASE $FEE_PROPORTIONAL $MIN_HTLC $TIMELOCK $CAPACITY_STD)

echo "channels count : $n_channels"

for i in `seq $1 $2`
do
    file_name="$i.csv"
    
    echo "----------creating-payments----------"
    python3 payment_generator.py $(($SEED + $i)) $SIMULATION_TIME $MRATES_FILE $AVERAGE_PAYMENT_AMOUNT $PAYMENT_AMOUNT_STD

    cd ./cloth
    bash ./run-simulation.sh $i ./output_dir/
    cd ..
    
    mv ./cloth/output_dir/channels_output.csv $result_dir/$CHANNEL_DATA_FOLDER/$file_name

    echo "----------------------------data-number-$i-generated----------------------------------"
done 

python3 real_lifeTime_aggrigator.py ./$result_dir/$CHANNEL_DATA_FOLDER $n_channels 1

cp ./lifeTimes_real.csv ./$result_dir/lifeTimes_real.csv
cp ./lifeTimes.csv ./$result_dir/lifeTimes.csv
cp ./Mrates.csv ./$result_dir/Mrates.csv
cp ./DataGenerator.sh ./$result_dir/DataGenerator.sh
cp ./cloth/cloth_input.txt ./$result_dir/cloth_input.txt
cp ./channels.csv ./$result_dir/channels.csv

echo "-----------------important-files-copied------------------"