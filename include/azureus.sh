#!/bin/bash

AZUHOME="$HOME/.Azureus"

LIBDIR="/usr/lib"


CLASSPATH="/usr/share/java/swt.jar:/usr/share/java/commons-cli.jar:/usr/share/java/log4j.jar:/usr/share/Azureus/Azureus.jar"

java -cp $CLASSPATH -Djava.library.path=$LIBDIR/swt org.gudy.azureus2.ui.common.Main --ui=swt
