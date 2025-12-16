#!/bin/bash

echo "Installing Monitor Everything (me)..."

if ! command -v pipx &> /dev/null; then
    echo "Error: pipx is not installed. Install it first:"
    echo "  macOS: brew install pipx"
    echo "  Linux: python3 -m pip install --user pipx"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "Error: git is not installed"
    exit 1
fi

INSTALL_DIR="${HOME}/.monitor_everything"

if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone https://github.com/kamaldhitalofficial/monitor_everything.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo "Installing package globally with pipx..."
pipx install -e "$INSTALL_DIR" --force

SHELL_CONFIG=""
if [ -n "$FISH_VERSION" ]; then
    SHELL_CONFIG="${HOME}/.config/fish/config.fish"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="${HOME}/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="${HOME}/.bashrc"
elif [ -f "${HOME}/.config/fish/config.fish" ]; then
    SHELL_CONFIG="${HOME}/.config/fish/config.fish"
elif [ -f "${HOME}/.zshrc" ]; then
    SHELL_CONFIG="${HOME}/.zshrc"
elif [ -f "${HOME}/.bashrc" ]; then
    SHELL_CONFIG="${HOME}/.bashrc"
fi

echo "✓ Installation complete!"
echo "The 'me' command is now available globally."
echo ""
if [ -n "$SHELL_CONFIG" ]; then
    echo "Restart your terminal or run: source $SHELL_CONFIG"
    echo "Then run: me setup"
else
    echo "Run: me setup"
fi
