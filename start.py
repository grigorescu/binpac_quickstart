#!/usr/bin/env python3
"""start.py - Create the boilerplate files for a new Zeek binpac analyzer

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
"""

from docopt import docopt
import os
import sys
from jinja2 import Template

def mkdir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno == 2:
            print("Could not create directory, permission denied.")
            sys.exit(1)
        if e.errno == 13:
            print("Could not create directory, source not found. Are you sure '%s' is the directory from Zeek's git?" % path)
            sys.exit(1)
        if e.errno == 17:
            print("Directory already exists. Refusing to overwrite files.")
            sys.exit(1)
        raise e

def main(arguments):
    # Split the optional namespace out of NAME
    if "::" in arguments['NAME']:
        (namespace,name) = arguments['NAME'].split("::",1)
    else:
        name = arguments['NAME']
        namespace = "Zeek"


    if arguments['--plugin']:
        pac_path = os.path.join(arguments['PATH_TO_ZEEK_SRC'], "src")
        if not os.path.exists(pac_path):
            os.makedirs(pac_path)
        script_path = os.path.join(arguments['PATH_TO_ZEEK_SRC'], "scripts")
        if not os.path.exists(script_path):
            os.makedirs(script_path)
        do_plugin = True
    else:
        pac_path = os.path.join(arguments['PATH_TO_ZEEK_SRC'], "src/analyzer/protocol", name.lower())
        script_path = os.path.join(arguments['PATH_TO_ZEEK_SRC'], "scripts/base/protocols", name.lower())
        do_plugin = False
        mkdir(pac_path)
        mkdir(script_path)

    # # 1. C stuff

    if do_plugin:
        fin = open("./templates/cmakelists_txt_plugin.jinja2", 'r')
    else:
        fin = open("./templates/cmakelists_txt.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    if do_plugin:
        fout = open(os.path.join(arguments['PATH_TO_ZEEK_SRC'], "CMakeLists.txt"), 'w')
    else:
        fout = open(os.path.join(pac_path, "CMakeLists.txt"), 'w')
    fout.write(template.render(name=name,space=namespace))
    fout.close()

    fin = open("./templates/plugin_cc.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "Plugin.cc"), 'w')
    fout.write(template.render(name=name, desc=arguments['DESCRIPTION'], space=namespace))
    fout.close()

    fin = open("./templates/protocol_cc.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s.cc" % name.upper()), 'w')
    fout.write(template.render(name=name, tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    fin = open("./templates/protocol_h.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s.h" % name.upper()), 'w')
    fout.write(template.render(name=name, tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    # 2. Events

    fin = open("./templates/events_bif.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "events.bif"), 'w')
    fout.write(template.render(name=name))
    fout.close()

    # 3. PAC files

    fin = open("./templates/protocol_pac.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s.pac" % name.lower()), 'w')
    fout.write(template.render(name=name, desc=arguments['DESCRIPTION']))
    fout.close()

    fin = open("./templates/protocol-protocol_pac.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s-protocol.pac" % name.lower()), 'w')
    fout.write(template.render(name=name))
    fout.close()

    fin = open("./templates/protocol-analyzer_pac.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(pac_path, "%s-analyzer.pac" % name.lower()), 'w')
    fout.write(template.render(name=name))
    fout.close()

    # 4. Scripts

    fin = open("./templates/load_zeek.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(script_path, "__load__.zeek"), 'w')
    fout.write(template.render(name=name))
    fout.close()

    fin = open("./templates/dpd_sig.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(script_path, "dpd.sig"), 'w')
    fout.write(template.render(name=name, tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    fin = open("./templates/main_zeek.jinja2", 'r')
    template = Template(fin.read())
    fin.close()
    fout = open(os.path.join(script_path, "main.zeek"), 'w')
    fout.write(template.render(name=name, tcp=arguments['--tcp'], udp=arguments['--udp']))
    fout.close()

    # 5. Add it to protocol/CMakeLIsts.txt

    if not do_plugin:
        fin = open(os.path.join(arguments['PATH_TO_ZEEK_SRC'], "src/analyzer/protocol", "CMakeLists.txt"), 'r')
        protocols = fin.readlines()
        fin.close()
        protocols.append("add_subdirectory(%s)\n" % name.lower())
        protocols.sort()
        fout = open(os.path.join(arguments['PATH_TO_ZEEK_SRC'], "src/analyzer/protocol", "CMakeLists.txt"), 'w')
        fout.writelines(protocols)
        fout.close()

    # 6. Add it to init-default.zeek
        fin = open(os.path.join(arguments['PATH_TO_ZEEK_SRC'], "scripts/base", "init-default.zeek"), 'r')
        init_default = fin.readlines()
        fin.close()
        load_cmd = "@load base/protocols/%s\n" % name.lower()
        for i in range(len(init_default)-1):
            if "@load base/protocols/" in init_default[i]:
                if load_cmd > init_default[i] and (load_cmd < init_default[i+1] or init_default[i+1] == '\n'):
                    init_default.insert(i+1, load_cmd)
                    break
        fout = open(os.path.join(arguments['PATH_TO_ZEEK_SRC'], "scripts/base", "init-default.zeek"), 'w')
        fout.writelines(init_default)
        fout.close()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
