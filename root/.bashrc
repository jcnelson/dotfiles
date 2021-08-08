export PATH="/bin:/usr/bin:/usr/bin:/usr/ucb:/sbin:/usr/sbin:/home/jude/bin:/usr/local/bin:/usr/local/sbin"

USER="$(whoami)"

PS1="[\$(ps1.sh)]:\w"

if [[ "$USER" == "root" ]]; then
    export PS1="$PS1# "
else
    export PS1="$PS1$ "
fi

export PAGER=less

alias l=ls
alias ll="ls -l"
alias la="ls -a"
alias vi=/usr/local/bin/vim
alias cat="catv"
alias make="make -j4"
alias su="su -"
alias grep="/usr/bin/grep --color"
alias fgrep="/usr/bin/grep --color -F"
alias egrep="/usr/bin/grep --color -E"
alias cp='cp -i'
alias rm='rm -i'
alias mv='mv -i'

export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"

export PYTHONPATH="$PYTHONPATH:/usr/local/lib/python2.7/site-packages"

source /usr/share/bash-completion/bash_completion
