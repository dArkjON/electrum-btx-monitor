#!/usr/bin/env python3
"""
ElectrumX Blockchain Monitor Script
Ruft wichtige Daten aus einem ElectrumX Docker-Container ab
"""

import subprocess
import json
import time
import datetime
import sys
from typing import Dict, List, Optional

class ElectrumMonitor:
    def __init__(self, container_name: str = "electrumx"):
        self.container_name = container_name
        self.rpc_cmd = f"docker exec {container_name} electrumx_rpc"

    def execute_rpc(self, command: str) -> Optional[Dict]:
        """Führt einen RPC-Befehl im Docker-Container aus"""
        try:
            result = subprocess.run(
                f"{self.rpc_cmd} {command}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"❌ Fehler bei RPC-Aufruf '{command}': {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout bei RPC-Aufruf '{command}'")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON-Decode-Fehler bei '{command}': {e}")
            return None
        except Exception as e:
            print(f"❌ Unerwarteter Fehler bei '{command}': {e}")
            return None

    def get_server_info(self) -> Optional[Dict]:
        """Holt grundlegende Server-Informationen"""
        return self.execute_rpc("getinfo")

    def get_peers(self) -> Optional[Dict]:
        """Holt Peer-Informationen"""
        return self.execute_rpc("peers")

    def get_sessions(self) -> Optional[Dict]:
        """Holt Session-Informationen"""
        return self.execute_rpc("sessions")

    def get_groups(self) -> Optional[Dict]:
        """Holt Gruppen-Informationen"""
        return self.execute_rpc("groups")

    def get_daemon_info(self) -> Optional[Dict]:
        """Holt Daemon-Informationen über die Blockchain-Verbindung"""
        # Versucht Daemon-URL und Status abzufragen
        info = self.get_server_info()
        if info and 'daemon' in info:
            return {
                'daemon_url': info['daemon'],
                'daemon_height': info.get('daemon height', 'N/A'),
                'db_height': info.get('db height', 'N/A')
            }
        return None

    def get_mempool_info(self) -> Dict:
        """Extrahiert Mempool-Informationen aus den Logs"""
        try:
            result = subprocess.run(
                f"docker logs {self.container_name} --tail 50 | grep 'MemPool:'",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split('\n')
                last_line = lines[-1] if lines else ""

                # Parse Mempool-Zeile
                if "txs" in last_line:
                    parts = last_line.split()
                    txs = "0"
                    size = "0.00"
                    addresses = "0"

                    for i, part in enumerate(parts):
                        if part == "txs" and i + 1 < len(parts):
                            txs = parts[i + 1].rstrip(',')
                        elif part == "MB" and i - 1 >= 0:
                            size = parts[i - 1]
                        elif part == "addresses" and i - 1 >= 0:
                            addresses = parts[i - 1]

                    return {
                        'transactions': txs,
                        'size_mb': size,
                        'addresses': addresses,
                        'last_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

            return {'transactions': '0', 'size_mb': '0.00', 'addresses': '0', 'last_update': 'N/A'}
        except Exception as e:
            print(f"⚠️  Konnte Mempool-Informationen nicht abrufen: {e}")
            return {'transactions': 'N/A', 'size_mb': 'N/A', 'addresses': 'N/A', 'last_update': 'N/A'}

    def get_network_stats(self) -> Dict:
        """Berechnet Netzwerk-Statistiken"""
        info = self.get_server_info()
        if not info:
            return {}

        return {
            'uptime': info.get('uptime', 'N/A'),
            'version': info.get('version', 'N/A'),
            'coin': info.get('coin', 'N/A'),
            'total_requests': info.get('request total', 0),
            'db_flush_count': info.get('db_flush_count', 0),
            'groups': info.get('groups', 0)
        }

    def get_request_stats(self) -> Dict:
        """Extrahiert Request-Statistiken"""
        info = self.get_server_info()
        if not info or 'request counts' not in info:
            return {}

        request_counts = info['request counts']
        total_requests = info.get('request total', 0)

        # Top-5 Requests
        top_requests = sorted(request_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            'total_requests': total_requests,
            'top_requests': dict(top_requests),
            'invalid_requests': request_counts.get('invalid method', 0)
        }

    def format_bytes(self, bytes_val: int) -> str:
        """Formatiert Bytes in lesbare Einheiten"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} TB"

    def print_dashboard(self):
        """Zeigt ein Dashboard mit allen wichtigen Informationen"""
        print("\n" + "="*60)
        print("🔷 ELECTRUMX BLOCKCHAIN MONITOR")
        print(f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        # Server-Info
        info = self.get_server_info()
        if info:
            print(f"\n🖥️  SERVER INFORMATION:")
            print(f"   Version: {info.get('version', 'N/A')}")
            print(f"   Coin: {info.get('coin', 'N/A')}")
            print(f"   Uptime: {info.get('uptime', 'N/A')}")
            print(f"   PID: {info.get('pid', 'N/A')}")

        # Blockchain-Status
        daemon_info = self.get_daemon_info()
        if daemon_info:
            print(f"\n⛓️  BLOCKCHAIN STATUS:")
            print(f"   Daemon URL: {daemon_info['daemon_url']}")
            print(f"   Daemon Height: {daemon_info['daemon_height']}")
            print(f"   DB Height: {daemon_info['db_height']}")
            if daemon_info['daemon_height'] != 'N/A' and daemon_info['db_height'] != 'N/A':
                sync_diff = int(daemon_info['daemon_height']) - int(daemon_info['db_height'])
                print(f"   Sync Status: {'✅ In Sync' if sync_diff == 0 else f'⚠️  Behind by {sync_diff} blocks'}")

        # Mempool-Info
        mempool = self.get_mempool_info()
        print(f"\n💾 MEMPOOL STATUS:")
        print(f"   Transactions: {mempool['transactions']}")
        print(f"   Size: {mempool['size_mb']} MB")
        print(f"   Addresses: {mempool['addresses']}")
        print(f"   Last Update: {mempool['last_update']}")

        # Request Statistics
        req_stats = self.get_request_stats()
        if req_stats:
            print(f"\n📊 REQUEST STATISTICS:")
            print(f"   Total Requests: {req_stats.get('total_requests', 0)}")

        # Cache Statistics
        if info:
            print(f"\n🗄️  CACHE STATISTICS:")
            print(f"   History Cache: {info.get('history cache', 'N/A')}")
            print(f"   Merkle Cache: {info.get('merkle cache', 'N/A')}")
            print(f"   TX Hashes Cache: {info.get('tx hashes cache', 'N/A')}")
            print(f"   TXs Sent: {info.get('txs sent', 0)}")

        # Network Info
        net_stats = self.get_network_stats()
        if net_stats:
            print(f"\n🌍 NETWORK STATISTICS:")
            print(f"   Groups: {net_stats.get('groups', 0)}")
            print(f"   DB Flush Count: {net_stats.get('db_flush_count', 0)}")

        print("\n" + "="*60)

    def monitor_loop(self, interval: int = 30):
        """Startet eine Endlosschleife zur Überwachung"""
        try:
            print(f"🚀 Starte ElectrumX Monitoring (Intervall: {interval}s)")
            print("Drücke STRG+C zum Beenden")

            while True:
                self.print_dashboard()
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n👋 Monitoring beendet")
        except Exception as e:
            print(f"\n❌ Fehler im Monitoring-Loop: {e}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="ElectrumX Blockchain Monitor")
    parser.add_argument("-c", "--container", default="electrumx",
                       help="Docker-Container Name (default: electrumx)")
    parser.add_argument("-i", "--interval", type=int, default=30,
                       help="Monitoring-Intervall in Sekunden (default: 30)")
    parser.add_argument("-o", "--once", action="store_true",
                       help="Nur einmal ausführen und beenden")
    parser.add_argument("-j", "--json", action="store_true",
                       help="Ausgabe als JSON")

    args = parser.parse_args()

    monitor = ElectrumMonitor(args.container)

    if args.json:
        # JSON-Modus
        data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'server_info': monitor.get_server_info(),
            'mempool': monitor.get_mempool_info(),
            'daemon_info': monitor.get_daemon_info()
        }

        # JSON-Ausgabe
        json_output = json.dumps(data, indent=2, default=str)
        print(json_output)

        # Speichere als status.json in /var/www/status/
        try:
            with open('/var/www/status/status.json', 'w') as f:
                f.write(json_output)
            print("✅ JSON-Datei gespeichert: /var/www/status/status.json")
        except Exception as e:
            print(f"❌ Fehler beim Speichern der JSON-Datei: {e}")
    elif args.once:
        # Einmalige Ausführung
        monitor.print_dashboard()
    else:
        # Kontinuierliches Monitoring
        monitor.monitor_loop(args.interval)

if __name__ == "__main__":
    main()