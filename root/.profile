export PATH="/root/bin:/home/jude/bin:$PATH:/sbin:/usr/sbin"

USER="$(whoami)"

if [ "$USER" == "root" ]; then
    export PS1="\h:\w# "
else
    export PS1="\u@\h:\w$ "
fi

export PAGER=less

alias l=ls
alias ll="ls -l"
alias la="ls -a"
alias vi=/usr/local/bin/vim
alias cat="cat -v"
alias make="make -j4"
alias su="su -"

LANG="en_US.UTF-8"
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL="en_US.UTF-8"

# OPAM configuration
# . /root/.opam/opam-init/init.sh > /dev/null 2> /dev/null || true
