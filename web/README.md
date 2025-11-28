# Web Dashboard

This directory contains the web dashboard files for the BTX ElectrumX Monitor.

## Files

- `index.html` - Main dashboard HTML file with embedded CSS and JavaScript
- `btx-logo.png` - Official Bitcore BTX logo (128x128px PNG)
- `README.md` - This file

## Usage

### Copy to Web Server
```bash
# Copy files to nginx web directory
sudo cp -r web/* /var/www/status/

# Set proper permissions
sudo chown -R www-data:www-data /var/www/status/
sudo chmod -R 644 /var/www/status/*
```

### Nginx Configuration
Add this to your Nginx site configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/status;
    index index.html;

    location /status.json {
        add_header Content-Type application/json;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
        try_files $uri =404;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## Features

- **Responsive Design**: Works on desktop and mobile devices
- **BTX Styling**: Professional Bitcore branding with blue/turquoise colors
- **Live Updates**: Auto-refreshes every 30 seconds
- **Progress Indicators**: Visual sync status bars
- **Error Handling**: Graceful error messages
- **Performance Metrics**: Real-time data display

## Dependencies

- Modern web browser with JavaScript support
- BTX ElectrumX Monitor script running with JSON output
- Web server (Nginx/Apache) for hosting

## Configuration

The dashboard automatically fetches data from `/status.json` on the same domain. Ensure your monitoring script is configured to output JSON to this location.

## SSL Support

For production use, configure SSL/TLS certificates. The dashboard works with both HTTP and HTTPS.

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+