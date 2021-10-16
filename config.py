config = {
    "title": "Demo",
    "desc": """<strong>Simple Digital Heartbeat</strong> is a lightweight pure HTML/CSS status page. You can easily add sections and execute custom bash command.<br /><br />The full documentation can be found on the <a
      href="https://github.com/Urban-Hacker/DigitalHeartbeat">github</a> page.""",
    "popup": "This message will be automatically displayed in case of one or more failure(s).",
    "sections": [
        {
            "title": "Internal Network",
            "tests": [
                {"name": "urbanhacker.net (web)",
                    "cmd": "curl -fsSL https://urbanhacker.net"},
                {"name": "failure example (web)",
                 "cmd": "curl -fsSL https://fail.urbanhacker.net"}
            ]
        },
        {
            "title": "External Network",
            "tests": [
                {"name": "DNS server 8.8.8.8 (ping)",
                 "cmd": "ping 8.8.8.8"},
                {"name": "linux.com (web)",
                    "cmd": "curl -fsSl https://linux.com"},
                {"name": "github.com (web)",
                    "cmd": "curl -fsSl https://github.com"},
            ]
        }
    ]
}
