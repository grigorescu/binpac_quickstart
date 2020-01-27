# BinPAC Quickstart

Create the boilerplate files for a new Zeek BinPAC analyzer.

## Installation

This requires Python 3 and Zeek 3. To install the dependencies:

`pip3 install -r requirements.txt`

## Tutorial

Please see: https://www.zeek.org/development/howtos/binpac-sample-analyzer.html

## Usage

```
start.py - Create the boilerplate files for a new Zeek binpac analyzer

Usage:
    start.py NAME DESCRIPTION PATH_TO_ZEEK_SRC (--tcp|--udp) [--buffered] [--plugin]


Arguments:
    NAME                 - Short name of protocol to be used in filenames (e.g. HTTP).  You may optionally
                           include a plugin namespace, eg "Space::NAME"  The default namespace is otherwise
                           just "Zeek".
    DESCRIPTION          - Long name of protocol (e.g. Hypertext Transfer Protocol)
    PATH_TO_ZEEK_SRC     - Full path to the Zeek source directory, where the files will be written.
                             e.g. ~/src/zeek-3.0/
                           NOTE: If you want to make changes in a git branch, you'll need to
                                 create and checkout the branch before running this script.

Options:
    --tcp                - Include the TCP analyzer class. You probably want this if this protocol uses TCP.
    --udp                - Include the UDP analyzer class. You probably want this if this protocol uses UDP.
    --buffered           - Enable the flow buffer, enabling use of &oneline and &length
                           in record types. Without this option, it will be a datagram analyzer,
                           which is faster but has no incremental input or buffering support.
   --plugin              - Create the BinPac files as a plugin. The path to the plugin is substituted for
                           the Zeek source directory (PATH_TO_ZEEK_SRC).
```

