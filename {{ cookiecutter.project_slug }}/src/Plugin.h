#pragma once

#include <plugin/Plugin.h>

namespace plugin {
namespace {{ cookiecutter.project_namespace }}_{{ cookiecutter.protocol_name }} {

class Plugin : public zeek::plugin::Plugin
{
protected:
	// Overridden from zeek::plugin::Plugin.
	zeek::plugin::Configuration Configure() override;
};

extern Plugin plugin;

}
}
