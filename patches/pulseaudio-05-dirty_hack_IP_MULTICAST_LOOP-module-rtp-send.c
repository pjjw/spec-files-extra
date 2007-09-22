--- pulseaudio-0.9.5/src/modules/rtp/module-rtp-send.c.orig	2006-08-25 01:56:34.000000000 +0200
+++ pulseaudio-0.9.5/src/modules/rtp/module-rtp-send.c	2007-09-22 21:44:32.618859180 +0200
@@ -263,7 +263,7 @@
     if (setsockopt(fd, IPPROTO_IP, IP_MULTICAST_LOOP, &loop, sizeof(loop)) < 0 ||
         setsockopt(sap_fd, IPPROTO_IP, IP_MULTICAST_LOOP, &loop, sizeof(loop)) < 0) {
         pa_log("IP_MULTICAST_LOOP failed: %s", pa_cstrerror(errno));
-        goto fail;
+        /* simply continue until completely fixed in Solaris (X86)  goto fail; */
     }
 
     pa_source_output_new_data_init(&data);
