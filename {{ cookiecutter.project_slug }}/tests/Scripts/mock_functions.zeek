## Installing with geoip can be tricky, so we'll mock this up for now.
global mock_lookup_location = function(a: addr) : geo_location {
	if ( a in 80.0.0.0/8 )
	    return [$country_code="RU"];
	return [$country_code="US"];
};

lookup_location = mock_lookup_location;