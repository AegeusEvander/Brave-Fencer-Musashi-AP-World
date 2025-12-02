#!/bin/bash

# Get the current directory
folder=$(dirname "$0")

# Create a temporary directory
temp_dir=$(mktemp -d)
mkdir $temp_dir/bfm

# Move into the folder
cd "$folder" || exit

# Get all files in the folder (excluding directories and the script file itself)
files=()
script_name=$(basename "$0")

while IFS= read -r -d $'\0' file; do
    if [[ ! -d "$file" && "$file" != "$script_name" && "$file" != "./sign_and_pack.sh" && "$file" != "./.gitignore" ]]; then
        files+=("$file")
    fi
done < <(find . -maxdepth 1 -type f ! -name "$script_name" -print0)

# Sign each file with GPG
for file in "${files[@]}"; do
    gpg --output "$temp_dir/bfm/$(basename "$file").sig" --detach-sign --digest-algo SHA256 "$file"
done

cp "${files[@]}" "$temp_dir/bfm"

cp -r "$folder/docs" "$temp_dir/bfm/docs"
cp -r "$folder/test" "$temp_dir/bfm/test"
cp -r "$folder/patch" "$temp_dir/bfm/patch"

cd "$temp_dir" || exit

cd "$folder" || exit

#cp "$temp_dir/bfm.apworld" "$HOME"
rsync -avq --delete "$temp_dir/bfm/" "$HOME/Documents/ArchipelagoSource/Archipelago/worlds/bfm/"

# Clean up temporary directory
rm -rf "$temp_dir"

cd "$HOME/Documents/ArchipelagoSource/Archipelago/"

python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 ModuleUpdate.py --yes --force
python3 Launcher.py "Build APWorlds" -- "Brave Fencer Musashi"

cp -f "build/apworlds/bfm.apworld" "$HOME/Documents/Archipelago6.4/Archipelago/custom_worlds"

cd "$folder"

echo "Files signed with GPG and packaged into an APWorld."
echo "Don't forget to increment the version!"
