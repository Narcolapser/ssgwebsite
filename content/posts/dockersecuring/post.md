# Securing a Docker Registry

## History you'll probably skip

I recently had a problem at work with our new container registry. I had set it up to be accessible to the outside world so that our pipe lines running in Azure could push docker images to said registry. However security had not open the firewall to allow traffic to come in. I put in the request through the appropriate channels and they informed me that TLS1.0 was enabled on the server. Well thats no, [TLS 1.0 and 1.1 were deprecated in 20202](https://en.wikipedia.org/wiki/Transport_Layer_Security). Easy solution though, I just disable TLS in the container registry.

Not seeing a simple flag for this in the documentation I went to the [forums](https://forums.docker.com/t/how-would-i-disable-tls-1-0-on-a-container-registry/103595). At time of writing the only response was a bot. Not only were there no other forum posts asking about this, no one on the forums seemed to care very much. So I acknowledge that this is (currently) a niche issue, but when some one else runs into this, I hope this will provide some insight.

# How to secure

Currently there is not official way to do this that I am aware of. So the easiest thing to do is to just proxy the container registry behind nginx. You can do this via an nginx container or installation, either way the configuration file is what matters and it ought to look something like this:


    server {
        listen      443 ssl;
        server_name  containers.example.com;
        ssl_certificate     /etc/nginx/conf.d/certificate.crt;
        ssl_certificate_key /etc/nginx/conf.d/certificate.key;
        ssl_protocols TLSv1.2;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers on;

        # optional for extra security
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        location / {
            proxy_pass https://127.0.0.1:8443;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

Advice found here:
https://reinout.vanrees.org/weblog/2017/05/02/https-behind-proxy.html


Notes:

I should attempt to create a secured container registry, ideally allow a simple drop in place replacement for the existing container registry. you simply replace "registry:2" with "narcolapser/tlsregistry:1.2" and all is well. 
