--- libupnp-1.6.0/README.orig	2007-07-15 15:19:30.541726415 +0700
+++ libupnp-1.6.0/README	2007-07-15 15:20:12.555440132 +0700
@@ -111,7 +111,7 @@
 options enabled (see below for options available at configure time).
 
 % cd $(LIBUPNP)
-% ./configure CFLAGS="-DSPARC_SOLARIS -mtune=<cputype> -mcpu=<cputype>"
+% ./configure CFLAGS="-DSOLARIS -mtune=<cputype> -mcpu=<cputype>"
 % make
 
 will build a Sparc Solaris version of the binaries without debug support
@@ -247,7 +247,7 @@
 described above. Only the call to ./configure has to be done using an
 additional parameter:
 
-./configure CFLAGS="-mcpu=<cputype> -mtune=<cputype> -DSPARC_SOLARIS"
+./configure CFLAGS="-mcpu=<cputype> -mtune=<cputype> -DSOLARIS"
 
 where <cputype> has to be replaced by the appropriate CPU tuning flag (e.g.
 "supersparc"). Afterwards
--- libupnp-1.6.0/upnp/src/api/upnpapi.c.orig	2007-07-15 15:18:13.268459532 +0700
+++ libupnp-1.6.0/upnp/src/api/upnpapi.c	2007-07-15 15:18:32.466823380 +0700
@@ -42,8 +42,7 @@
 	#include <netinet/in.h>
 	#include <arpa/inet.h>
 
-	#ifndef SPARC_SOLARIS
-//		#include <linux/if.h>
+	#ifndef SOLARIS
 		#include <net/if.h>
 	#else
 		#include <fcntl.h>
--- libupnp-1.6.0/upnp/src/genlib/net/uri/uri.c.orig	2007-07-15 15:16:44.866909688 +0700
+++ libupnp-1.6.0/upnp/src/genlib/net/uri/uri.c	2007-07-15 15:17:11.248388785 +0700
@@ -627,7 +627,7 @@
         // platform-specific stuff below
 #if defined(WIN32) || defined(__CYGWIN__)
         h=gethostbyname(temp_host_name);
-#elif defined(SPARC_SOLARIS)
+#elif defined(SOLARIS)
         errCode = gethostbyname_r( temp_host_name,
                                    &h,
                                    temp_hostbyname_buff,
--- libupnp-1.6.0/threadutil/inc/iasnprintf.h.orig	2007-07-15 15:15:42.003910263 +0700
+++ libupnp-1.6.0/threadutil/inc/iasnprintf.h	2007-07-15 15:16:02.790286791 +0700
@@ -50,7 +50,7 @@
 	       int incr,
 	       int max,
 	       const char * fmt, ...)
-#ifndef SPARC_SOLARIS
+#ifndef SOLARIS
  #if (__GNUC__ >= 3)
 	__attribute__((format (__printf__, 4, 5)));
  #else
