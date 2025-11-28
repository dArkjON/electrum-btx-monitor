# BTX ElectrumX Monitor

A comprehensive monitoring tool for Bitcore (BTX) ElectrumX servers that provides real-time blockchain status, mempool information, and performance metrics via a web dashboard and JSON API.

## 🚀 Features

### Monitor & Display
- **Real-time Blockchain Status**: Block height, sync status, daemon connection
- **Server Information**: Version, uptime, process ID
- **Mempool Analytics**: Transaction count, size, active addresses
- **Performance Metrics**: Request counts, groups, DB flush statistics
- **Professional Web Dashboard**: BTX-styled responsive interface

### Output Formats
- **Web Dashboard**: Beautiful HTML interface with live updates
- **JSON API**: Machine-readable status data
- **Command Line**: Text-based dashboard for terminal use

## 📋 Requirements

- Python 3.6+
- Docker with running ElectrumX container
- Nginx (optional, for web dashboard hosting)
- Cron (optional, for automatic updates)

## 🛠️ Installation

### 1. Clone or Download
```bash
# Clone the repository
git clone https://github.com/dArkjON/electrum-btx-monitor.git
cd electrum-btx-monitor

# Or download the script directly
wget https://raw.githubusercontent.com/dArkjON/electrum-btx-monitor/main/electrum_monitor.py
```

### 2. Make Executable
```bash
chmod +x electrum_monitor.py
```

### 3. Verify Docker Container
Ensure your ElectrumX container is running and accessible:
```bash
docker ps | grep electrum
```

## 📖 Usage

### Command Line Interface

```bash
# Display current status once
python3 electrum_monitor.py --once

# Continuous monitoring (updates every 30 seconds)
python3 electrum_monitor.py

# Custom refresh interval (60 seconds)
python3 electrum_monitor.py --interval 60

# Output as JSON
python3 electrum_monitor.py --json

# Custom container name
python3 electrum_monitor.py --container my-electrumx
```

### Web Dashboard Setup

#### 1. Configure Nginx
Create a new Nginx configuration file:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/status;
    index index.html;

    location /status.json {
        add_header Content-Type application/json;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        try_files $uri =404;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

#### 2. Setup Web Files
```bash
mkdir -p /var/www/status
# Copy or download the HTML dashboard to /var/www/status/index.html
```

#### 3. Automated Updates
Set up a cron job for automatic JSON updates:

```bash
# Edit cron jobs
crontab -e

# Add this line for 30-minute updates
*/30 * * * * /usr/bin/python3 /path/to/electrum_monitor.py --json > /dev/null 2>&1
```

## 🌐 Web Dashboard

The web dashboard provides:

- **Responsive Design**: Works on desktop and mobile devices
- **BTX Branding**: Professional Bitcore styling with official logo
- **Live Updates**: Auto-refreshes every 30 seconds
- **Progress Indicators**: Visual sync status and performance metrics
- **Error Handling**: Graceful degradation when ElectrumX is unavailable

### Access URLs
- Dashboard: `http://your-domain.com/`
- JSON API: `http://your-domain.com/status.json`

## 📊 JSON Output Structure

```json
{
  "timestamp": "2025-11-28T17:32:21.538526",
  "server_info": {
    "coin": "Bitcore",
    "version": "ElectrumX 1.15.0",
    "uptime": "14d 03h 47m",
    "daemon height": 1706493,
    "db height": 1706493,
    "request total": 1535,
    "db_flush_count": 7853,
    "groups": 702
  },
  "mempool": {
    "transactions": "0",
    "size_mb": "0.00",
    "addresses": "0",
    "last_update": "2025-11-28 17:32:22"
  },
  "daemon_info": {
    "daemon_url": "172.21.0.11:8556/",
    "daemon_height": 1706493,
    "db_height": 1706493
  }
}
```

## 🔧 Configuration

### Environment Variables
- **Default Container**: `electrumx` (override with `--container`)
- **Default Interval**: 30 seconds (override with `--interval`)
- **Output Directory**: Current working directory

### Docker Container Requirements
The monitored ElectrumX container must have:
- Accessible Docker daemon
- `electrumx_rpc` command available inside container
- Proper network connectivity

## 🐛 Troubleshooting

### Common Issues

**"Docker container not found"**
```bash
# Check container name
docker ps
# Use correct container name with --container flag
```

**"Permission denied"**
```bash
# Ensure executable permissions
chmod +x electrum_monitor.py
# Check Docker daemon access
sudo usermod -aG docker $USER
```

**"ElectrumX RPC error"**
```bash
# Test RPC manually
docker exec electrumx electrumx_rpc getinfo
```

### Debug Mode
Enable verbose output by removing output redirection in cron jobs:
```bash
*/30 * * * * /usr/bin/python3 /path/to/electrum_monitor.py --json >> /var/log/electrum_monitor.log 2>&1
```

## 📝 Changelog

### v1.0.0
- Initial release
- Basic monitoring functionality
- Web dashboard with BTX styling
- JSON API output
- Automatic updates via cron
- SSL/HTTPS support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚡ Support

- **Issues**: [GitHub Issues](https://github.com/dArkjON/electrum-btx-monitor/issues)
- **Documentation**: This README file
- **Community**: Bitcore Discord/Telegram groups

## 🙏 Acknowledgments

- [Bitcore](https://bitcore.cc/) - The BTX blockchain project
- [ElectrumX](https://github.com/spesmilo/electrumx) - Electrum server implementation
- Nginx - Web server for hosting the dashboard
- Let's Encrypt - SSL certificates for secure access

---

**Made with ❤️ for the Bitcore (BTX) Community**