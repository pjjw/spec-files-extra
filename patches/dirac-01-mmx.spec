--- dirac-0.7.0/configure.ac.orig	2007-07-13 19:15:23.996374023 +0700
+++ dirac-0.7.0/configure.ac	2007-07-13 19:16:22.467662141 +0700
@@ -346,7 +346,13 @@
 AC_ARG_ENABLE(mmx, AC_HELP_STRING([--enable-mmx], [enable MMX optimization (default=yes)]), [enable_mmx="${enableval}"], [enable_mmx="yes"])
 
 if test x"${enable_mmx}" = x"yes" ; then
-	case "$CXX" in
+	case "$( basename $CXX )" in
+	    CC*)
+			AC_LANG_PUSH(C++)
+			TRY_CFLAGS="-xarch=sse"
+			AC_TRY_CXXFLAGS([#include <mmintrin.h>],[], [$TRY_CFLAGS $CXXFLAGS],[CXXFLAGS="$CXXFLAGS $TRY_CFLAGS -DHAVE_MMX"])
+			AC_LANG_POP(C++)
+			;;
 	    g++*)
 			AC_LANG_PUSH(C++)
 			TRY_CFLAGS="-mmmx"
