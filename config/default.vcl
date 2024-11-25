#
# VARNISH CONFIG FILE USED FOR trace.trentwiles.com
# Additionally contains configuration for api-sle.trentwil.es
#

# Assumes server is running on port 8000
# Caches everything except for /

vcl 4.0;

import std;

backend bart {
    .host = "127.0.0.1";
    .port = "10394";
}

backend trace {
    .host = "127.0.0.1";
    .port = "8000";
}

sub vcl_recv {

    if (req.http.host ~ "trace\.trentwiles\.com") {
        set req.backend_hint = trace;
        # cache everything for trace.trentwiles.com
        unset req.http.Cookie;
        set req.http.X-Cache-TTL = "31536000s"; # Cache for 1 year
        if (req.url == "/") {
            return (pass); # Don't cache homepage
        }
    } else if (req.http.host ~ "bart\.trentwil\.es") {
        set req.backend_hint = bart;


        if (req.url ~ "^/($|api/v1/stations|api/v1/trains)") {
            unset req.http.Cookie;
        }

        if (req.url == "/") {
            set req.http.X-Cache-TTL = "31536000s"; # Cache / for 1 year
        } else if (req.url ~ "^/api/v1/stations/") {
            set req.http.X-Cache-TTL = "604800s"; # Cache /api/v1/stations/* for 1 week
        } else if (req.url ~ "^/api/v1/trains/") {
            set req.http.X-Cache-TTL = "300s"; # Cache /api/v1/trains/ for 5 minutes
        } else if (req.url ~ "^/api/v1/fares") {
            return (pass); # Don't cache /api/v1/fares
        } else {
            set req.http.X-Cache-TTL = "86400s"; # Cache everything else for 1 day
        }
    } else {
        set req.backend_hint = bart;
        set req.http.X-Cache-TTL = "86400s"; # Cache everything else for 1 day
    }
}

sub vcl_backend_response {
    if (bereq.http.X-Cache-TTL) {
        set beresp.ttl = std.duration(bereq.http.X-Cache-TTL, 1s);
    }

    # server header removed for security
    unset beresp.http.Server;
}

sub vcl_deliver {
    # hit/miss header
    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT";
    } else {
        set resp.http.X-Cache = "MISS";
    }

    unset resp.http.Server;
    unset resp.http.X-Varnish;
    unset resp.http.Via;
}