if [ $# -lt 2 ]
then
    echo "usage: $0 <data count> <outputdir>"
    exit
fi

echo "----------------------------------start-genenation-------------------------------------"

rm -r $2
mkdir $2

for i in `seq 1 $1`
do
    file_name="$i.csv"

    cd ./cloth
    # bash ./run-simulation.sh $i ./output_dir/
    ./cloth ./output_dir/
    cd ..
    
    mv ./cloth/output_dir/channels_output.csv $2/$file_name

    echo "----------------------------data-number-$i-generated----------------------------------"
done 