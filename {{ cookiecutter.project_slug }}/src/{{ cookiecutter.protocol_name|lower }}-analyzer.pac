# Generated by binpac_quickstart

refine flow {{ cookiecutter.protocol_name }}_Flow += {
	function proc_{{ cookiecutter.protocol_name|lower }}_message(msg: {{ cookiecutter.protocol_name }}_PDU): bool
		%{
		BifEvent::generate_{{ cookiecutter.protocol_name|lower }}_event(connection()->bro_analyzer(), connection()->bro_analyzer()->Conn());
		return true;
		%}
};

refine typeattr {{ cookiecutter.protocol_name }}_PDU += &let {
	proc: bool = $context.flow.proc_{{ cookiecutter.protocol_name|lower }}_message(this);
};