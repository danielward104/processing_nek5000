# Confirm the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Please specify path to files."
    echo "Exiting."
    exit 1
fi

path_to_files=${1}

nfiles=$(ls -1q ${path_to_files}plume0.f* | wc -l)

for i in $(seq -f "%05g" 1 20 ${nfiles})
do
   echo plume0.f$i >> ${path_to_files}files_to_copy.txt
done
