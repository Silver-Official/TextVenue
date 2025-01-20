#!/bin/bash

echo "Creating the OS.."

# Prompt the user to select a file
echo "Please select a file to use for the OS creation process:"
file=$(zenity --file-selection --title="Select a file for OS creation")

# Check if a file was selected
if [ -z "$file" ]; then
  echo "No file selected. Exiting."
  exit 1
fi

# Your OS creation logic using the selected file
echo "Using file: $file for OS creation process, checking if GRUB is installed on this device..."
sudo apt-get install -y grub

# Enter text mode to edit the selected file
echo "Enter text mode"
nano "$file"

# Prompt the user if more files are needed
echo "Need more files?"
PS3="Please choose an option: "
options=("Yes" "No")
select opt in "${options[@]}"; do
    case $opt in
        "Yes")
            while true; do
                read -p "Enter file name (or 'done' to finish): " filename
                if [ "$filename" == "done" ]; then
                    break
                fi
                touch "$filename"
                echo "File '$filename' created."
            done
            break
            ;;
        "No")
            echo "Okay, skipping!"
            break
            ;;
        *)
            echo "Error: Invalid option, choose Yes or No"
            ;;
    esac
done

# Test the OS or get packages if needed
echo "Test your OS now (or get packages if this is based off of a Linux distro or other...)"
chroot $file

echo "Publish this OS? (will create a iso.)"
PS3="Please choose an option: "
options=("Yes" "No")
select opt in "${options[@]}"; do
    case $opt in
        "Yes")
            genisoimage -o $file.iso -V "TextVenueVolume" $file
            echo "Created the ISO!"
            done
            break
            ;;
        "No")
            echo "Okay, skipping!"
            done
            break
            ;;
        *)
            echo "Error: Invalid option, choose Yes or No"
            ;;
    esac
done
