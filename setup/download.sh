#!/usr/bin/env bash

# TODO: Convert to python with requests, argparse, etc.
#  download all years, stop when 404

set -Eeuo pipefail
IFS=$'\n\t'

year=$1

if [ -z "${AOC_SESSION:-}" ]; then
  echo "error: Missing AOC_SESSION" >&2
  exit 1
fi

if [ ! -e "site/static/style.css" ]; then
  mkdir -p "site/static"

  echo "Downloading static/style.css"
  curl "https://adventofcode.com/static/style.css" -o "site/static/style.css"
fi

if [ ! -e "site/$year/index.html" ]; then
  mkdir -p "site/$year"

  echo "Downloading $year root"
  curl "https://adventofcode.com/$year" -o "site/$year/index.html" --cookie "session=$AOC_SESSION"
fi

for day in $(seq 25); do

  mkdir -p "site/$year/day/$day"

  if [ ! -e "site/$year/day/$day/index.html" ]; then
    echo "Downloading $year day $day"
    curl "https://adventofcode.com/$year/day/$day" -o "site/$year/day/$day/index.html" --cookie "session=$AOC_SESSION"
  fi
done

echo "Done"
