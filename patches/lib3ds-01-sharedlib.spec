diff -ur lib3ds-1.2.0-orig/configure.in lib3ds-1.2.0/configure.in
--- lib3ds-1.2.0-orig/configure.in	2002-01-14 19:09:15.000000000 +0700
+++ lib3ds-1.2.0/configure.in	2007-05-06 23:50:32.506940093 +0700
@@ -1,5 +1,6 @@
 dnl Process this file with autoconf to produce a configure script.
 AC_INIT(Makefile.am)
+AC_PROG_LIBTOOL
 
 #
 # Making releases:
@@ -38,8 +39,6 @@
 
 dnl Checks for programs.
 AC_PROG_CC
-AC_PROG_RANLIB
-CONFIGURE_GLUT(,)
 
 AC_MSG_CHECKING([for debugging mode])
 AC_ARG_ENABLE(debug-mode,   
diff -ur lib3ds-1.2.0-orig/examples/Makefile.am lib3ds-1.2.0/examples/Makefile.am
--- lib3ds-1.2.0-orig/examples/Makefile.am	2002-01-14 19:27:45.000000000 +0700
+++ lib3ds-1.2.0/examples/Makefile.am	2007-05-06 23:52:49.761942175 +0700
@@ -22,27 +22,22 @@
 
 INCLUDES = \
   -I$(top_srcdir) \
-  @GLUT_CFLAGS@ \
   @DMALLOC_CFLAGS@
 
-if GLUT_CHECK
 PLAYER = player
-else
-PLAYER = 
-endif
 
 noinst_PROGRAMS = \
   3ds2rib \
   $(PLAYER)
 
 LDADD = \
-  $(top_builddir)/lib3ds/lib3ds.a \
+  $(top_builddir)/lib3ds/lib3ds.la \
   @DMALLOC_LIBS@ -lm
 
 player_SOURCES = player.c
 player_LDADD = \
-  $(top_builddir)/lib3ds/lib3ds.a \
-  @GLUT_LIBS@ \
+  $(top_builddir)/lib3ds/lib3ds.la \
+  -lglut -lGL -lGLU \
   @DMALLOC_LIBS@ -lm
 
 
diff -ur lib3ds-1.2.0-orig/examples/glstub.h.in lib3ds-1.2.0/examples/glstub.h.in
--- lib3ds-1.2.0-orig/examples/glstub.h.in	2001-07-20 23:40:16.000000000 +0700
+++ lib3ds-1.2.0/examples/glstub.h.in	2007-05-06 23:51:06.152032929 +0700
@@ -1 +1 @@
-#include <@GLUT_HEADER_DIR@/glut.h>
+#include <GL/glut.h>
diff -ur lib3ds-1.2.0-orig/lib3ds/Makefile.am lib3ds-1.2.0/lib3ds/Makefile.am
--- lib3ds-1.2.0-orig/lib3ds/Makefile.am	2002-01-14 19:27:45.000000000 +0700
+++ lib3ds-1.2.0/lib3ds/Makefile.am	2007-05-06 23:50:32.507167001 +0700
@@ -24,9 +24,10 @@
 
 INCLUDES = -I$(top_srcdir)
 
-lib_LIBRARIES = lib3ds.a
+lib_LTLIBRARIES = lib3ds.la
+lib3ds_la_LDFLAGS = -version-info 1 -release 2
 
-lib3ds_a_SOURCES = \
+lib3ds_la_SOURCES = \
   io.c \
   float.c \
   vector.c \
diff -ur lib3ds-1.2.0-orig/tools/Makefile.am lib3ds-1.2.0/tools/Makefile.am
--- lib3ds-1.2.0-orig/tools/Makefile.am	2002-01-14 19:27:45.000000000 +0700
+++ lib3ds-1.2.0/tools/Makefile.am	2007-05-06 23:50:32.507313290 +0700
@@ -29,7 +29,7 @@
   3ds2m 
 
 LDADD = \
-  $(top_builddir)/lib3ds/lib3ds.a \
+  $(top_builddir)/lib3ds/lib3ds.la \
   @DMALLOC_LIBS@ -lm
 
 MANPAGES = \
