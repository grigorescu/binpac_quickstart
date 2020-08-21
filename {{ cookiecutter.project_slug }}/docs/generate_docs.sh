#! /usr/bin/env bash

set -e

# Our directory structure
dir=$( cd "$( dirname "$0" )" && pwd )
source_dir=$( cd "$dir"/.. && pwd )
output_dir=$source_dir/docs
build_dir=$source_dir/build

conf_file=$build_dir/zeekygen-test.conf
zeek_error_file=$build_dir/zeekygen-test-stderr.txt

scripts_output_dir=$output_dir/scripts

mkdir -p "$build_dir"
rm -rf "$scripts_output_dir"
mkdir -p "$scripts_output_dir"

# Configure Zeek
unset ZEEK_DISABLE_ZEEKYGEN;

export ZEEK_ALLOW_INIT_ERRORS=1
DEFAULT_ZEEKPATH=$(zeek-config --zeekpath)
export ZEEKPATH="$source_dir/scripts:$DEFAULT_ZEEKPATH"

# Run Zeek
function run_zeek
    {
    if ! zeek -b -B zeekygen -X "$conf_file" "$1" >/dev/null 2>"$zeek_error_file"
    then
        echo "Failed running zeek with zeekygen config file $conf_file"
        echo "See stderr in $zeek_error_file"
        exit 1
    fi
    }

# For each module (Namespace::Module), run it through zeek, and generate package documentation
cd "$source_dir"/scripts
find * -maxdepth 1 -mindepth 1 -type d -print0 | while IFS="" read -r -d $'\0' namespace
do
    (cat <<EOF
script	$namespace/*	$scripts_output_dir/
package	$namespace	$output_dir/index.rst
EOF
) > "$conf_file"
	run_zeek "$namespace"
done

# Finally, we fix the links from the upstream Zeek docs
find . -name '*.rst' -exec sed -i '' -e 's% </scripts/base% <zeek:scripts/base%g' -e 's% </scripts/policy% <zeek:scripts/policy%g' {} +

cd -
