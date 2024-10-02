ls -d */ > dirs.txt
cwd=$(pwd)

mkdir -p image_copy

while read dirs;
do
    num=${#dirs}
    if test $num -eq 8; then
        mkdir -p image_copy/${dirs}
        cp ${dirs}processing/images/vertical_velocity/* ./image_copy/${dirs}
    fi
done < dirs.txt
rm dirs.txt
