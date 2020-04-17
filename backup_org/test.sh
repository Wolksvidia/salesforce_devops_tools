#!/bin/bash
##functions
usage()
{
    echo "usage: script arguments [[[-f output_xml_filename ] [-a org_alias ] [-i for interactive mode]] | [-h]]"
}
##main
alias=
interactive=
filename=./package.xml

if [ $# -gt 0 ]; then    
    while [ "$1" != "" ]; do
        case $1 in
            -f | --file )           shift
                                    filename=$1
                                    ;;
            -a | --alias )          shift
                                    alias=$1
                                    ;;
            -i | --interactive )    interactive=1
                                    ;;
            -h | --help )           usage
                                    exit
                                    ;;
            * )                     usage
                                    exit 1
        esac
        shift
    done
else
    usage
    exit 1
fi

# Test code to verify command line processing

if [ "$interactive" = "1" ]; then
	echo "interactive is on"
    #set -x >> for debugg mode
    sfdx force:org:list
    echo -n "Enter name of the org > "
    read response
    if [ -n "$response" ]; then
        org=$response
    fi
    sfdx force:org:display -u $org --json
    #set +x
else
	echo "interactive is off"
    sfdx force:org:display -u $alias --json
fi
echo "output file = $filename"