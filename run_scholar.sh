#!/bin/bash

keyword=$1
alias_f=$2
end_year=$3
start_year=$4

echo "$start_year" "$end_year" "$keyword" "$alias_f"
call_python_script() {
    python3 scholarly-byKeyword.py "$start_year" "$end_year" "$keyword" "$alias_f"
} 

while true; do
    if [ "$end_year" -lt "$start_year" ]; then
        echo "End year is less than start year. Stopping the script."
        exit 0
    fi

    call_python_script

    echo "Python script called with start_year=$start_year and end_year=$end_year"

    end_year=$((end_year - 1))

    sleep 3600
done