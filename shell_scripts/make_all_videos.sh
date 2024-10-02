ls -d */ > dirs.txt
cwd=$(pwd)

while read dirs;
do
    num=${#dirs}
    if test $num -eq 8; then

        cd ${dirs}processing
        echo 2 | make_video
        cd ${cwd}

    fi
done < dirs.txt

rm dirs.txt
