syntax on
set nu
let g:molokai_original = 1
set t_Co=256
colorscheme molokai
map <space>e :tabnew 
map <space>f :tabp<CR>
map <space>g :tabn<CR>
map <space>v :vs 
map <space>d :vert diffsplit 
set scrolloff=6
set completeopt=preview,menu 
set cursorline
"set autoindent
set tabstop=4
"set softtabstop=4
set shiftwidth=4
set expandtab
set enc=utf-8
set langmenu=zh_CN.UTF-8
set helplang=cn
set mouse=
set selection=exclusive
set selectmode=mouse,key
"set foldmethod=syntax
"set foldenable
"set smartindent
"自动补全
":inoremap ( ()<ESC>i
":inoremap ) <c-r>=ClosePair(')')<CR>
":inoremap { {<CR>}<ESC>O
":inoremap } <c-r>=ClosePair('}')<CR>
":inoremap [ []<ESC>i
":inoremap ] <c-r>=ClosePair(']')<CR>
":inoremap " ""<ESC>i
":inoremap ' ''<ESC>i
"function! ClosePair(char)
"    if getline('.')[col('.') - 1] == a:char
"        return "\<Right>"
"    else
"        return a:char
"    endif
"endfunction
"定义函数SetTitle，自动插入文件头 
autocmd BufNewFile *.cpp,*.sh,*.java,*.py,*.c,*.cu,*.cc,*.h,*.hpp exec ":call SetTitle()"
func SetTitle() 
    if &filetype == 'sh' 
        call setline(1,"\#########################################################################") 
        call append(line("."), "\# Author: Huang Di") 
        call append(line(".")+1, "\# Mail: hd232508@163.com") 
        call append(line(".")+2, "\# Created Time: ".strftime("%c")) 
        call append(line(".")+3, "\#########################################################################") 
        call append(line(".")+4, "\#!/bin/bash") 
        call append(line(".")+5, "") 
    elseif &filetype == 'python'
        call setline(1,"#########################################################################") 
        call append(line("."), "# Author: Huang Di") 
        call append(line(".")+1, "# Mail: hd232508@163.com") 
        call append(line(".")+2, "# Created Time: ".strftime("%c")) 
        call append(line(".")+3, "#########################################################################") 
        call append(line(".")+4, "") 
    else 
        call setline(1, "/*************************************************************************") 
        call append(line("."), "    > Author: Huang Di") 
        call append(line(".")+1, "    > Mail: hd232508@163.com ") 
        call append(line(".")+2, "    > Created Time: ".strftime("%c")) 
        call append(line(".")+3, " ************************************************************************/") 
        call append(line(".")+4, "")
    endif
    autocmd BufNewFile * normal G
endfunction
