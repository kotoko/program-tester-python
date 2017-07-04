# program-tester.py
Script for simple testing executable programs.

## Description
Script was created during my attempts in Informatic Olympic. With the passing of time script had more features, so I decided to publish it.

Script runs specified program on multiple tests and compare the program's output with the expected test's output. Test's input must have `*.in` extension and test's output must have `*.out` extension. Script only checks standard output, error output is ignored.

You have to get tests on your own :)

## Features
* run program on all tests from specified folder
* run program on only specified tests from specified folder
* display only tests' results that failed
* display all tests' results
* display beginning of comparison of outputs, if test failed 
* display currently executing test's name
* measure execution time
* display user-friendly results with colors

## Installation
Following commands should be done in linux console.

### Minimal installation
Download script `program-tester.py`:

    wget -O program-tester.py https://github.com/kotoko/program-tester-python/raw/master/program-tester.py

Add execution permission:

    chmod +x program-tester.py

And run:

    ./program-tester

Done!

### Full installation
Advantages of full installation: easy update, translation support, convenient running. Following programs must be already installed: **git**, **gettext**, **make**. I'm assuming you using bash. If not, make appropriate adjustments.

Download the project:

    git clone https://github.com/kotoko/program-tester-python.git -b master --single-branch ~/.program-tester

Add execution permission:

    chmod +x ~/.program-tester/program-tester.py

Create file `~/.program-tester-update.sh`:

    nano -w ~/.program-tester-update.sh

And paste there code for updater:

```bash
#!/bin/sh
# script's installation directory
DIRECTORY="$HOME/.program-tester"

show_error_and_exit ()
{
    echo "$@"
    exit 1
}

# check directory
[ ! -d "$DIRECTORY" ] && show_error_and_exit "Missing directory: $DIRECTORY"

# go to directory
cd "$DIRECTORY" >/dev/null 2>&1 || show_error_and_exit "Failed to go into directory: $DIRECTORY"

# clenup directory
git reset --hard origin/master >/dev/null 2>&1 || show_error_and_exit "Failed to reset state of project"
git clean -f -d >/dev/null 2>&1 || show_error_and_exit "Failed to remove garbage files"

# update script
git pull >/dev/null 2>&1 || show_error_and_exit "Failed to download update"

# set executable permissions
chmod +x program-tester.py >/dev/null 2>&1 || show_error_and_exit "Failed to add executable permission"

# generate translations
make clean >/dev/null 2>&1 || show_error_and_exit "Failed to delete old translations' binaries"
make all >/dev/null 2>&1 || show_error_and_exit "Failed to generate translations' binaries"

echo "Updated successfully!"
exit
```

Save file and close editor. Add execution permission for updater:

    chmod +x ~/.program-tester-update.sh

Add aliases for convenient usage:

    echo 'alias program-tester="~/.program-tester/program-tester.py"' >> ~/.bash_aliases
    echo 'alias program-tester-update="~/.program-tester-update.sh"' >> ~/.bash_aliases

At the end restart all consoles, which was already launched. Logging out and then logging in should be sufficient.

Done!

If you want to run script:

    program-tester

If you want to update script:

    program-tester-update

## TODO
- [ ] measure memory used by program
- [ ] do not run program second time to measure time

