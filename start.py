#!/usr/bin/env python2
"""start.py - Create the boilerplate files for a new Bro binpac analyzer

Usage:
    start.py NAME DESCRIPTION PATH_TO_BRO_SRC (--tcp|--udp) [--buffered] [--plugin]


Arguments:
    NAME                 - Short name of protocol to be used in filenames (e.g. HTTP)
    DESCRIPTION          - Long name of protocol (e.g. Hypertext Transfer Protocol)
    PATH_TO_BRO_SRC      - Full path to the Bro source directory, where the files will be written.
                             e.g. ~/src/bro-2.2/
                           NOTE: If you want to make changes in a git branch, you'll need to
                                 create and checkout the branch before running this script.

Options:
    --tcp                - Include the TCP analyzer class. You probably want this if this protocol uses TCP.
    --udp                - Include the UDP analyzer class. You probably want this if this protocol uses UDP.
    --buffered           - Enable the flow buffer, enabling use of &oneline and &length
                           in record types. Without this option, it will be a datagram analyzer,
                           which is faster but has no incremental input or buffering support.
   --plugin              - Create the BinPac files as a plugin. The path to the plugin is substituted for
                           the Bro source directory (PATH_TO_BRO_SRC).
"""

from docopt import docopt
import os
import sys
from jinja2 import Template

def mkdir(path):
    try:
        os.mkdir(path)
    except OSError, e:
        if e.errno == 2:
            print "Could not create directory, permission denied."
            sys.exit(1)
        if e.errno == 13:
            print "Could not create directory, source not found. Are you sure '%s' is the directory from Bro's git?" % path
            sys.exit(1)
        if e.errno == 17:
            print "Directory already exists. Refusing to overwrite files."
            sys.exit(1)
        raise e

def main(arguments):
    if arguments['--plugin']:
        pac_path = os.path.join(arguments['PATH_TO_BRO_SRC'], "src")
        script_path = os.path.join(arguments['PATH_TO_BRO_SRC'], "scripts")
        do_plugin = True
    else:
        pac_path = os.path.join(arguments['PATH_TO_BRO_SRC'], "src/analyzer/protocol", arguments['NAME'].lower())
        script_path = os.path.join(arguments['PATH_TO_BRO_SRC'], "scripts/base/protocols", arguments['NAME'].lower())
        do_plugin = False
        mkdir(pac_path)
        mkdir(script_path)

    # # 1. C stuff

    if do_plugin:
	fin = open("./templates/cmakelists_txt_plugin.jinja2",'r')
    else:
	fin = open("./templates/cmakelists_txt.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    if do_plugin:
        fout = open(os.path.join(arguments['PATH_TO_BRO_SRC'], "CMakeLists.txt"), 'w')
    else:
        fout = open(os.path.join(pac_path, "CMakeLists.txt"), 'w')
    fout.write(template.render(name=arguments['NAME']))
    fout.close()

    fin = open("./templates/plugin_cc.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "Plugin.cc"), 'w')
    fout.write(template.render(name=arguments['NAME'], desc=arguments['DESCRIPTION']))
    fout.close()

    fin = open("./templates/protocol_cc.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s.cc" % arguments['NAME'].upper()), 'w')
    fout.write(template.render(name=arguments['NAME'], tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    fin = open("./templates/protocol_h.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s.h" % arguments['NAME'].upper()), 'w')
    fout.write(template.render(name=arguments['NAME'], tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    # 2. Events

    fin = open("./templates/events_bif.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "events.bif"), 'w')
    fout.write(template.render(name=arguments['NAME']))
    fout.close()

    # 3. PAC files

    fin = open("./templates/protocol_pac.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s.pac" % arguments['NAME'].lower()), 'w')
    fout.write(template.render(name=arguments['NAME'], desc=arguments['DESCRIPTION']))
    fout.close()

    fin = open("./templates/protocol-protocol_pac.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s-protocol.pac" % arguments['NAME'].lower()), 'w')
    fout.write(template.render(name=arguments['NAME']))
    fout.close()

    fin = open("./templates/protocol-analyzer_pac.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s-analyzer.pac" % arguments['NAME'].lower()), 'w')
    fout.write(template.render(name=arguments['NAME']))
    fout.close()

    # 4. Scripts

    fin = open("./templates/load_bro.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(script_path, "__load__.bro"), 'w')
    fout.write(template.render(name=arguments['NAME']))
    fout.close()

    fin = open("./templates/dpd_sig.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(script_path, "dpd.sig"), 'w')
    fout.write(template.render(name=arguments['NAME'], tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    fin = open("./templates/main_bro.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(script_path, "main.bro"), 'w')
    fout.write(template.render(name=arguments['NAME'], tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    # 5. Add it to protocol/CMakeLIsts.txt

    if not do_plugin:
        fin = open(os.path.join(arguments['PATH_TO_BRO_SRC'], "src/analyzer/protocol", "CMakeLists.txt"), 'r')
        protocols = fin.readlines()
        fin.close()
        protocols.append("add_subdirectory(%s)\n" % arguments['NAME'].lower())
        protocols.sort()
        fout = open(os.path.join(arguments['PATH_TO_BRO_SRC'], "src/analyzer/protocol", "CMakeLists.txt"), 'w')
        fout.writelines(protocols)
        fout.close()

    # 6. Add it to init-default.bro
        fin = open(os.path.join(arguments['PATH_TO_BRO_SRC'], "scripts/base", "init-default.bro"), 'r')
        init_default = fin.readlines()
        fin.close()
        load_cmd = "@load base/protocols/%s\n" % arguments['NAME'].lower()
        for i in range(len(init_default)-1):
            if "@load base/protocols/" in init_default[i]:
                if load_cmd > init_default[i] and (load_cmd < init_default[i+1] or init_default[i+1] == '\n'):
                    init_default.insert(i+1, load_cmd)
                    break
        fout = open(os.path.join(arguments['PATH_TO_BRO_SRC'], "scripts/base", "init-default.bro"), 'w')
        fout.writelines(init_default)
        fout.close()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
