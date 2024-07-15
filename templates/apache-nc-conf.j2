Listen {{ cs_nc_port }}
<VirtualHost *:{{ cs_nc_port }}>
    DocumentRoot {{ cs_nc_web_root_dir }}/
    ServerName {{cs_nc_domain}}
    <IfModule mod_headers.c>
        Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains"
        Header always set X-Content-Type-Options "nosniff"
        Header always set X-XSS-Protection "1; mode=block"
        Header always set X-Robots-Tag "none"
        Header always set X-Frame-Options "SAMEORIGIN"
        Header always set Referrer-Policy "no-referrer"
    </IfModule>
    <Directory {{ cs_nc_web_root_dir }}/>
        Require all granted
        AllowOverride All
        Options FollowSymLinks MultiViews
        <IfModule mod_dav.c>
            Dav off
        </IfModule>
        Satisfy Any
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/nextcloud_error.log
    CustomLog ${APACHE_LOG_DIR}/nextcloud_access.log combined
    
    SSLEngine on
    SSLCertificateFile /etc/ssl/{{ cs_nc_domain }}/fullchain.pem
    SSLCertificateKeyFile /etc/ssl/{{ cs_nc_domain }}/privkey.pem
    SSLProtocol             all -SSLv3 -TLSv1 -TLSv1.1 -TLSv1.2
    SSLHonorCipherOrder     off
    SSLSessionTickets       off

</VirtualHost>
SSLUseStapling On
SSLStaplingCache "shmcb:logs/ssl_stapling(32768)"
