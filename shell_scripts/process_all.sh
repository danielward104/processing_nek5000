ls -d */ > dirs.txt
cwd=$(pwd)

while read dirs;
do
    num=${#dirs}
    if test $num -eq 8; then

        cd ${dirs}
        process_files
        qsub run_python.sh
        cd ${cwd}

    fi
done < dirs.txt
