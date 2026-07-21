echo "Installing TagFetch for Linux"
sudo wget https://github.com/elitrycraft/tagfetch/releases/download/1.0.3R/TagFetch_linux_x86_64 -O "/usr/bin/tagfetch"
sudo chmod +x /usr/bin/tagfetch

if [ -f /usr/bin/tagfetch ]; then
  echo "TagFetch has been successfully installed."
else
  echo "TagFetch not installed"
