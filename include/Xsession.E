#!/bin/ksh 
#####################################################################
###  File:              Xsession.xfce  Version 0.1 $Revision: 1.0 $
###
###  Default Location:  /usr/dt/config/Xsession.xfce
###
###  Purpose:           Xfce session start script
###
###  Invoked by:        Solaris Desktop Login Manager (dtlogin)
###
#####################################################################

DTDSPMSG=/usr/dt/bin/dtdspmsg

export SESSIONTYPE="altDt"
export SDT_ALT_SESSION="/usr/dt/config/Xsession2.E"
export SDT_ALT_HELLO="/bin/true"
export SDT_NO_TOOLTALK="1"
export SDT_NO_DTDBCACHE="1"
export START_SPECKEYSD="no"

exec /usr/dt/bin/Xsession
