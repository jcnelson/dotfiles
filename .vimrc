" All system-wide defaults are set in $VIMRUNTIME/debian.vim (usually just
" /usr/share/vim/vimcurrent/debian.vim) and sourced by the call to :runtime
" you can find below.  If you wish to change any of those settings, you should
" do it in this file (/etc/vim/vimrc), since debian.vim will be overwritten
" everytime an upgrade of the vim packages is performed.  It is recommended to
" make changes after sourcing debian.vim since it alters the value of the
" 'compatible' option.

" Source a global configuration file if available
if filereadable("/etc/vim/vimrc.local")
  source /etc/vim/vimrc.local
endif

" Uncomment the next line to make Vim more Vi-compatible
" NOTE: debian.vim sets 'nocompatible'.  Setting 'compatible' changes numerous
" options, so any other options should be set AFTER setting 'compatible'.
"set compatible
set nocompatible

" To disable a plugin, add it's bundle name to the following list
let g:pathogen_disabled = ['vim-solidity', 'syntastic']

execute pathogen#infect()

behave xterm

" Vim5 and later versions support syntax highlighting. Uncommenting the next
" line enables syntax highlighting by default.
syntax on

" If using a dark background within the editing area and syntax highlighting
" turn on this option as well
set background=dark

" Uncomment the following to have Vim jump to the last position when
" reopening a file
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" Uncomment the following to have Vim load indentation rules and plugins
" according to the detected filetype.
if has("autocmd")
  filetype plugin indent on
endif

" The following are commented out as they cause vim to behave a lot
" differently from regular Vi. They are highly recommended though.
set showcmd		" Show (partial) command in status line.
set showmatch		" Show matching brackets.
set ignorecase		" Do case insensitive matching
set smartcase		" Do smart case matching
set incsearch		" Incremental search
set autowrite		" Automatically save before commands like :next and :make
set hidden             " Hide buffers when they are abandoned
set wildmenu       " TAB autocomplete for comands
set mouse=a		" Enable mouse usage (all modes)
set tabstop=4
set shiftwidth=3
set expandtab
set backspace=2

" search
set hlsearch
nnoremap ,<space> :nohlsearch<CR>

" cursor line
set cursorline
hi CursorLine   cterm=NONE ctermbg=darkblue ctermfg=white guibg=darkblue guifg=white

autocmd WinEnter * setlocal cursorline
autocmd WinLeave * setlocal nocursorline

" Paste code without indents
nnoremap <F2> :set invpaste paste?<CR>
set pastetoggle=<F2>

set showmode
set number

" Start NERDTree automatically if no files are given
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif

" Disable unicode arrows in NERDTree
let g:NERDTreeDirArrows = 0

" quit if NERDTree is the last window open
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif

" NERDTree file filter
let NERDTreeIgnore = ['\.pyc$', '\~$']

" Ctrl-A becomes "select all"
map <C-a> <esc>ggVG<CR>

" allows cursor change in tmux mode
if exists('$TMUX')
    let &t_SI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=1\x7\<Esc>\\"
    let &t_EI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=0\x7\<Esc>\\"
else
    let &t_SI = "\<Esc>]50;CursorShape=1\x7"
    let &t_EI = "\<Esc>]50;CursorShape=0\x7"
endif

" wrap 80 chars for tex, etc
au BufRead,BufNewFile *.tex setlocal textwidth=80
au BufRead,BufNewFile *.md setlocal textwidth=80

" let g:syntastic_sol_checkers = ['syntastic-solidity-solc', 'syntastic-solidity-solium']

nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

set timeoutlen=1000
set ttimeoutlen=0

command DiffOrig vert new | set bt=nofile | r # | 0d_ | diffthis | wincmd p | diffthis

autocmd Filetype javascript setlocal ts=2 sts=2 sw=2
autocmd Filetype javascript setlocal colorcolumn=100
autocmd Filetype markdown setlocal ts=3 sts=3 sw=3 colorcolumn=80

set ruler

