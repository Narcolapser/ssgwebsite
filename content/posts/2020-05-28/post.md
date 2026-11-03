# Python is wonderful

## The challenge

Just a quick exultation here. I love python. We have a service that used a PHP backend to log get requests into a CSV. When we migrated to a new server, it broke, and nobody knew how to fix PHP. I spent 2.5h trying to fix it. I then told my boss I could either continue banging my head or write a python script to do it. The latter would probably be faster. He green lite the python option, and away I went. Thursday morning at 8:30, I started and was told it would be good to have it by Monday. By 9:15, I had written the script, commented it, set up version control, and installed it as a service.

## The script

The big time-saver here was avoiding Apache or Nginx. And this is made possible by python's built-in Http server. While not a recommended tool for a production environment, it is amazing because it is simple for serving basic utilities. The bulk of the script was just the parsing of the binary strings of the query string into a dictionary for easy formatting. But the three keys were:

1. Extending BaseHTTPRequestHandler with a new do_GET method.
2. httpd = HTTPServer(('0.0.0.0', 80), {The extended handler from point 1})
3. httpd.serve_forever()

That's all it took to create a webserver that covered all my needs. Amazing. I love it.

## The service

I'd be remised if I didn't also mention how simple systemd was. It needs a description, path to a file to execute, and a state inclusion. The last one (WantedBy=multi-user.target) isn't intuitive, but it's simple to slap on to everything and call it good. Beyond that:

        cp cdprpy.service /etc/systemd/system
        systemctl daemon-reload
        systemctl enable cdprpy
        systemctl start cdprpy

Done. Ah, this was a satisfying morning.
