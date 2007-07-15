--- libupnp-1.6.0/upnp/src/genlib/net/http/webserver.c.orig	2007-07-15 15:25:26.661244198 +0700
+++ libupnp-1.6.0/upnp/src/genlib/net/http/webserver.c	2007-07-15 15:26:05.370982319 +0700
@@ -290,7 +290,7 @@
 *	 0 - On Sucess														
 *	 UPNP_E_OUTOF_MEMORY - on memory allocation failures				
 ************************************************************************/
-UPNP_INLINE int
+int
 get_content_type( IN const char *filename,
                   OUT DOMString * content_type )
 {
