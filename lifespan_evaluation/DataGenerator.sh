if [ $# -lt 3 ]
then
    echo "usage: $0 <data count> <outputdir>"
    exit
fi

echo "----------------------------------start-genenation-------------------------------------"

rm -r $3
mkdir $3

for i in `seq $1 $2`
do
    file_name="$i.csv"

    cd ./cloth
    bash ./run-simulation.sh $i ./output_dir/
    cd ..
    
    mv ./cloth/output_dir/channels_output.csv $3/$file_name

    echo "----------------------------data-number-$i-generated----------------------------------"
done 