#!/bin/ksh 
#####################################################################
###  File:              Xsession2.E  Version 0.1 $Revision: 1.0 $
###
###  Default Location:  /usr/dt/config/Xsession2.E
###
###  Purpose:           Enlightenment Desktop start script
###
###  Invoked by:        /usr/dt/bin/Xsession
###
#####################################################################

# First a little namespace cleanup of vars associated with this
# (and /usr/dt/bin/Xsession.ow) scripts.

unset SDT_ALT_SESSION
unset SDT_ALT_HELLO
unset SDT_NO_DSDM

if [ -f /etc/dt/config/Xinitrc.E ]; then
    XINITRC="/etc/dt/config/Xinitrc.E"
else
    XINITRC="/usr/dt/config/Xinitrc.E"
fi

if [ -x /usr/dt/bin/xmbind ]; then
    /usr/dt/bin/xmbind
fi

echo 'Enlightenment'

if [ -f $XINITRC ]; then
    echo "using xinitrc file: $XINITRC"
    /bin/ksh $XINITRC
else
    echo "xinitrc file: $XINITRC not found"
fi

