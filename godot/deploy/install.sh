#!/usr/bin/env bash
# Installs the game's server (godot/client/server, ENet over UDP with DTLS) on an Ubuntu VM
# (Oracle Cloud Always Free, x86_64 or ARM) as a systemd service that starts with the machine.
#
#   curl -fsSL https://raw.githubusercontent.com/sapega89/Path-Of-A-Warrior/dev/godot/deploy/install.sh | sudo bash
#
# Run it again to update the server to the latest dev. The accounts stay in /var/lib/pow-server.
# Afterwards: the certificate the game must trust is /var/lib/pow-server/server.crt.
set -euo pipefail

GODOT_VERSION="${GODOT_VERSION:-4.5.1}"
BRANCH="${BRANCH:-dev}"
REPO="${REPO:-https://github.com/sapega89/Path-Of-A-Warrior.git}"
PORT="${PORT:-28310}"
APP=/opt/pow-server
DATA=/var/lib/pow-server

[ "$(id -u)" = 0 ] || { echo "run with sudo"; exit 1; }

apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git unzip curl ca-certificates \
    fontconfig iptables-persistent > /dev/null

case "$(uname -m)" in
    x86_64) GODOT_ARCH=x86_64 ;;
    aarch64) GODOT_ARCH=arm64 ;;
    *) echo "unsupported CPU $(uname -m)"; exit 1 ;;
esac
GODOT=/usr/local/bin/godot
if ! "$GODOT" --version 2>/dev/null | grep -q "^${GODOT_VERSION}\."; then
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/godot.zip" \
        "https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_linux.${GODOT_ARCH}.zip"
    unzip -q "$tmp/godot.zip" -d "$tmp"
    install -m 755 "$tmp/Godot_v${GODOT_VERSION}-stable_linux.${GODOT_ARCH}" "$GODOT"
    rm -rf "$tmp"
fi

id pow >/dev/null 2>&1 || useradd --system --home "$DATA" --shell /usr/sbin/nologin pow
mkdir -p "$DATA"
chown pow:pow "$DATA"

if [ -d "$APP/.git" ]; then
    git -C "$APP" fetch -q --depth 1 origin "$BRANCH"
    git -C "$APP" reset -q --hard "origin/$BRANCH"
else
    git clone -q --depth 1 --branch "$BRANCH" "$REPO" "$APP"
fi
chown -R pow:pow "$APP"
# the import cache (.godot/) the server's scenes and scripts load from
sudo -u pow HOME="$DATA" timeout 600 "$GODOT" --headless --path "$APP/godot/client" --import > /dev/null 2>&1 || true

cat > /etc/systemd/system/pow-server.service <<UNIT
[Unit]
Description=Path of a Warrior game server (UDP ${PORT}, ENet + DTLS)
After=network-online.target
Wants=network-online.target

[Service]
User=pow
Environment=HOME=${DATA}
ExecStart=${GODOT} --headless --path ${APP}/godot/client res://server/main.tscn -- --port ${PORT} --data ${DATA}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable -q pow-server
systemctl restart pow-server

# Oracle's Ubuntu images reject everything but SSH in iptables: let the game's UDP port in.
if ! iptables -C INPUT -p udp --dport "$PORT" -j ACCEPT 2>/dev/null; then
    iptables -I INPUT 1 -p udp --dport "$PORT" -j ACCEPT
    netfilter-persistent save > /dev/null
fi

for _ in $(seq 1 30); do [ -f "$DATA/server.crt" ] && break; sleep 1; done
IP=$(curl -fsS -4 https://ifconfig.me 2>/dev/null || hostname -I | cut -d' ' -f1)
echo
echo "Server: ${IP}:${PORT} (UDP).  Logs: journalctl -u pow-server -f"
echo "Also open UDP ${PORT} in the VCN's Security List (Ingress, source 0.0.0.0/0)."
echo "The certificate the game must trust (copy it into godot/client/net/server.crt):"
echo
cat "$DATA/server.crt"
