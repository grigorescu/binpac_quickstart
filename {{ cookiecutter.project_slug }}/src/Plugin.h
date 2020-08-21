#pragma once

#include <plugin/Plugin.h>

namespace plugin {
namespace {{ cookiecutter.project_namespace }}_{{ cookiecutter.protocol_name }} {

class Plugin : public plugin::Plugin
{
protected:
	// Overridden from plugin::Plugin.
	plugin::Configuration Configure() override;
};

extern Plugin plugin;

}
}
