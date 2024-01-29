for file in /home/ubuntu/fullstack/DiceAndTiles-Backend/media/images/*.jpg; do
    filename=$(basename "$file")
    extension="${filename##*.}"
    filename_noext="${filename%.*}"
    output_file="/home/ubuntu/fullstack/DiceAndTiles-Backend/mediaWEBP/images/${filename_noext}.webp"
    cwebp "$file" -o "$output_file"
done
