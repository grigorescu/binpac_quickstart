# Generated by binpac_quickstart

signature dpd_{{ cookiecutter.protocol_name|lower }} {
	{% if tcp %}
	ip-proto == tcp
	{% elif udp %}
	ip-proto == udp
	{% endif %}

	# ## TODO: Define the payload. When Bro sees this regex, on
	# ## any port, it will enable your analyzer on that
	# ## connection.
	# ## payload /^{{ cookiecutter.protocol_name|upper }}/

	enable "{{ cookiecutter.protocol_name|lower }}"
}
