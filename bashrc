# .bashrc
if [ "$TERM" == "xterm" ]; then
    # No it isn't, it's gnome-terminal
    export TERM=xterm-256color
fi
if [ "$TERM" == "screen" ]; then
    # No it isn't, it's gnome-terminal
    export TERM=screen-256color
fi
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h \[\033[01;34m\]\w \[\033[00m\]\$ '
# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
alias ca='conda activate'
source /tools/module_env.sh
export HOME=/lustre/S/huangdi
export PATH=$HOME/perl5/bin:/bin:/usr/lib64/qt-3.3/bin:/home/huangdi/perl5/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/ibutils/bin:/home/huangdi/.local/bin:/home/huangdi/bin
export LD_LIBRARY_PATH=$HOME/perl5/lib/5.26.1
export PERL5LIB=$HOME/perl5/lib/5.26.1
#export PATH=$HOME/cuda-10.0/bin:$PATH
#export LD_LIBRARY_PATH=$HOME/cuda-10.0/lib64
#export PATH=/usr/local/cuda-10.1/bin:$PATH
#export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64
export PYTHONPATH=$HOME/embedding_transformer/
export PYTHONPATH=$HOME/wino3d/python/:$PYTHONPATH
export PYTHONPATH=$HOME/pytorch_winoconv/:$PYTHONPATH
export PYTHONPATH=$HOME/models/:$PYTHONPATH
#source $HOME/environs/embed-env/bin/activate
#source $HOME/environs/binary/bin/activate
#source $HOME/environs/binary/bin/activate
export PATH=$HOME/anaconda3/bin:$PATH




#export PATH="/lustre/S/guojiaming/build/gcc_compile/bin:$PATH"
#export C_INCLUDE_PATH=$C_INCLUDE_PATH:/lustre/S/guojiaming/build/gcc_compile/include
#export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/lustre/S/guojiaming/build/gcc_compile/include
#
#export LD_LIBRARY_PATH=/lustre/S/guojiaming/build/gcc_compile/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
#export LIBRARY_PATH=$LIBRARY_PATH:/lustre/S/guojiaming/build/gcc_compile/lib
#
#export LD_LIBRARY_PATH=/lustre/S/guojiaming/build/mpfr-4.1.0/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
#
#export CC=/lustre/S/guojiaming/build/gcc_compile/bin/gcc
#export CXX=/lustre/S/guojiaming/build/gcc_compile/bin/g++
#
##export LD_LIBRARY_PATH=/home/guojiaming/.mujoco/mjpro150/bin${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}



### openmpi
export PATH="/home/huangdi/openmpi/bin:$PATH"
export LD_LIBRARY_PATH="/home/huangdi/openmpi/lib/:$LD_LIBRARY_PATH"

module load cuda-cudnn/10.1-7.6.5
#module load cuda-cudnn/10.0-7.4.2
module load gcc/7.5.0
module load git/2.17.1 
module load slurm-tools

export LD_LIBRARY_PATH=/tools/cluster-software/cuda-cudnn/cuda-10.0-7.4.2/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# deepfill for cuda-9.0-7.0.5 tensorflow-gpu==1.7.0
alias cuda9='export PATH=$HOME/cuda-9.0-7.0.5/bin:$PATH;export LD_LIBRARY_PATH=$HOME/cuda-9.0-7.0.5/lib64:$LD_LIBRARY_PATH'

alias sq='slurm-gpu-queue'
alias si='slurm-gpu-info'
alias sb='sbatch'
alias sm='slurm-gpu-queue --me'
alias newest='ls -lt ./ | grep "ret*" | head -n 1 |awk '\''{print $9}'\'' | xargs tail -f'
alias valid='python ~/scripts/whohasgpu.py'
alias sbat='~/scripts/sbatch.sh'

alias v00='ssh gpu-v00'
alias v01='ssh gpu-v01'
alias v02='ssh gpu-v02'
alias v03='ssh gpu-v03'
alias v04='ssh gpu-v04'
alias v05='ssh gpu-v05'
alias v06='ssh gpu-v06'
alias v07='ssh gpu-v07'
alias v08='ssh gpu-v08'
alias v09='ssh gpu-v09'
alias v10='ssh gpu-v10'
alias v11='ssh gpu-v11'
alias v12='ssh gpu-v12'
alias v13='ssh gpu-v13'
alias v14='ssh gpu-v14'
alias v15='ssh gpu-v15'
alias v16='ssh gpu-v16'
alias v17='ssh gpu-v17'
alias v18='ssh gpu-v18'
alias v19='ssh gpu-v19'
alias t00='ssh gpu-t00'
alias t01='ssh gpu-t01'
alias t04='ssh gpu-t04'
alias t05='ssh gpu-t05'
alias t06='ssh gpu-t06'
alias t07='ssh gpu-t07'
alias t08='ssh gpu-t08'
alias t09='ssh gpu-t09'
alias t10='ssh gpu-t10'
alias t11='ssh gpu-t11'
alias t12='ssh gpu-t12'
alias t13='ssh gpu-t13'
alias a00='ssh gpu-a00'
alias a01='ssh gpu-a01'
alias a02='ssh gpu-a02'
alias a03='ssh gpu-a03'
alias a04='ssh gpu-a04'
alias a05='ssh gpu-a05'
alias a06='ssh gpu-a06'
alias a07='ssh gpu-a07'
alias a10='ssh gpu-a10'
alias a11='ssh gpu-a11'
alias a12='ssh gpu-a12'
alias a13='ssh gpu-a13'
alias a14='ssh gpu-a14'
alias a15='ssh gpu-a15'
alias f00='ssh eda-f00'
alias f01='ssh eda-f01'
alias f02='ssh eda-f02'
alias f03='ssh eda-f03'

# for rm {{
# mkdir ~/.delete, when rm somethings ,mv them to here
if [ ! -d $HOME/.delete ]
then
    mkdir $HOME/.delete
fi
unDoRm() {
  mv -i $HOME/.delete/$@ ./
}
toBackup()
{
    for thing in $@
    do
        echo $thing | grep '^-' > /dev/null
        if [ ! $? = 0 ]
        then
            mv $thing $HOME/.delete
#            echo mv $thing to ~/.delete, you can backup them
        fi
    done

}
cleanDelete()
{
    echo 'clean files in .delete?[y/N]'
    read confirm
    [ $confirm = 'y' ] || [ $confirm = 'Y' ]  && /usr/bin/rm -rf $HOME/.delete/*
}
# rm somethings
alias rm=toBackup
# see what in~/.delete now
alias lsdel='ls $HOME/.delete'
# undo
alias unrm=unDoRm
# clean ~/.delete
alias cleandel=cleanDelete
# cp
alias cp='cp -i'
# }}

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/lustre/S/huangdi/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/lustre/S/huangdi/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/lustre/S/huangdi/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/lustre/S/huangdi/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
 
# .bashrc
if [ "$TERM" == "xterm" ]; then
    # No it isn't, it's gnome-terminal
    export TERM=xterm-256color
fi
if [ "$TERM" == "screen" ]; then
    # No it isn't, it's gnome-terminal
    export TERM=screen-256color
fi
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h \[\033[01;34m\]\w \[\033[00m\]\$ '
# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
