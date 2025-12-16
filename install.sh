#!/bin/bash

echo "Installing Monitor Everything (me)..."

if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Install it first: curl -LsSf https://astral.sh/uv/install.sh | sh"
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

echo "Setting up virtual environment..."
uv venv .venv
source .venv/bin/activate

echo "Installing package..."
uv pip install -e .

SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="${HOME}/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="${HOME}/.bashrc"
elif [ -f "${HOME}/.zshrc" ]; then
    SHELL_CONFIG="${HOME}/.zshrc"
elif [ -f "${HOME}/.bashrc" ]; then
    SHELL_CONFIG="${HOME}/.bashrc"
fi

if [ -n "$SHELL_CONFIG" ]; then
    if ! grep -q "alias me=" "$SHELL_CONFIG"; then
        echo "alias me='${INSTALL_DIR}/.venv/bin/me'" >> "$SHELL_CONFIG"
        echo "✓ Added 'me' alias to $SHELL_CONFIG"
    fi
    echo "✓ Installation complete!"
    echo "Run: source $SHELL_CONFIG && me setup"
else
    echo "✓ Installation complete!"
    echo "Run: ${INSTALL_DIR}/.venv/bin/me setup"
fi
