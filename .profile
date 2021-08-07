#!/bin/bash

export PATH="/home/jude/bin:/usr/local/bin:/usr/local/sbin:/bin:/usr/bin:/usr/ucb:/sbin:/usr/sbin:/home/jude/.go/bin:/home/jude/.cargo/bin"

USER="$(whoami)"

# PS1="[\$(ps1.sh)]:\w"
PS1="\u@\h:\w"

if [[ "$USER" == "root" ]]; then
    export PS1="$PS1# "
else
    export PS1="$PS1$ "
fi

export PAGER=less

alias ls="ls --color"
alias l=ls
alias ll="ls -l"
alias la="ls -a"
alias vi=/usr/local/bin/vim
alias cat="cat -v"
alias make="make -j4"
alias su="su -"
alias grep="/bin/grep --color"
alias fgrep="/bin/grep --color -F"
alias egrep="/bin/grep --color -E"
alias top="/bin/busybox top"
alias jq="jq -S"
alias tmux="tmux -2"

export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"

export PYTHONPATH="/usr/local/lib/python2.7/site-packages"
export GOPATH="$HOME/.go"

# source /usr/share/bash-completion/bash_completion

# OPAM configuration
# . /home/jude/.opam/opam-init/init.sh > /dev/null 2> /dev/null || true

# make key-signing work
export GPG_TTY="$(tty)"

# export NIM_LIB_PREFIX="/home/jude/pkg/nim-0.18.0/"

# no more beeping
xset -b

# activate inputrc
bind -f ~/.inputrc

# The next line updates PATH for the Google Cloud SDK.
# if [ -f '/home/jude/google-cloud-sdk/path.bash.inc' ]; then . '/home/jude/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
# if [ -f '/home/jude/google-cloud-sdk/completion.bash.inc' ]; then . '/home/jude/google-cloud-sdk/completion.bash.inc'; fi

# export NVM_DIR="$HOME/.nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
# [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

alias xpdf="echo 'use zathura'; zathura"

export TERM=screen-256color
