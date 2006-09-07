#
# Default settings for GNOME packages on Solaris
#
# Portions Copyright 2006 Sun Microsystems, Inc.
# Author: laca@sun.com and others
#
SUNW_ProdName:             SpecFilesExtra
SUNW_ProdVers:             1.0

# Note: you need JDS CBE 1.4.1 or later for these 3:
%{?!jds_version:#}SUNW_Pkg_AllZones:         false
%{?!jds_version:#}SUNW_Pkg_Hollow:           false
%{?!jds_version:#}SUNW_Pkg_ThisZone:         false

# the version of JDS this is based on:
%define default_pkg_version 2.14.1
%{?jds_version:#}%define jds_version JDSosol
%define default_category   SFE,application
%define support_level      unsupported
%define cc_is_gcc %(test "x`basename $CC`" = xgcc && echo 1 || echo 0)
%define build_l10n %{?_with_l10n:1}%{?!_with_l10n:0}
%define debug_build %{?_with_debug:1}%{?!_with_debug:0}
%define is_nevada %(test `uname -r` = 5.11 && echo 1 || echo 0)

SUNW_Category:             %{default_category}
SUNW_HotLine:              Please contact your local service provider
SUNW_MaxInst:              1000
SUNW_Rev:		   110.0.4.%(date +%Y.%m.%d.%H.%M)
SUNW_Copyright:            default-copyright.txt
Vendor:			   http://pkgbuild.sf.net/spec-files-extra

%define _libexecdir        %{_prefix}/lib
%define _mandir		   %{_datadir}/man

%if %debug_build
%define _ldflags
%else
%define _ldflags           -Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect
%endif

%ifarch sparcv9
%define	_arch64		   sparcv9
%endif

%ifarch amd64
%define _arch64            amd64
%endif

%if %debug_build
%define pkgbuild_postprocess /bin/true
%define _cc_opt_level      -g
%define _cc64_opt_level    -g
%define _cxx_opt_level     -g
%else
%if %cc_is_gcc
%define _cc_opt_level      -O2
%define _cc64_opt_level    -O2
%define _cxx_opt_level     -O2
%else
%define _cc_opt_level      -xO4 -xspace
%define _cc64_opt_level    -xO2 -xspace
%define _cxx_opt_level     -xO3 -xspace
%endif
%endif

%if %cc_is_gcc

%define picflags -fPIC -DPIC

%ifarch sparc
%define optflags           %_cc_opt_level -mv8plus -Xlinker -i %picflags
%define cxx_optflags       %_cxx_opt_level -mv8plus -Xlinker -i %picflags
%define optflags64	   %_cc_opt_level -mcpu=ultrasparc -m64 -Xlinker -i %picflags
%endif

%ifarch i386
%define optflags           %_cc_opt_level -march=i586 -Xlinker -i -fno-omit-frame-pointers %picflags
%define cxx_optflags       %_cc_opt_level -march=i586 -Xlinker -i -fno-omit-frame-pointers %picflags
%define optflags64	   %_cc64_opt_level -march=opteron -m64 -Xlinker -i -fno-omit-frame-pointers %picflags
%endif

%else
# cc is not gcc

%define picflags -KPIC

%ifarch sparc
%define optflags           -i %_cc_opt_level -xstrconst -xarch=v8a -mr
%define cxx_optflags       -i %_cxx_opt_level -xarch=v8a -mr -norunpath
%define optflags64	   -i %_cc_opt_level -xstrconst -xarch=v9 -xcode=pic32 -mr
%endif

%ifarch i386
%define optflags           -i %_cc_opt_level -xstrconst -xpentium -mr -xregs=no%%frameptr
%define cxx_optflags       -i %_cxx_opt_level -pentium -mr -norunpath -xregs=no%%frameptr
%define optflags64	   -i -xarch=generic64 -Kpic -xregs=no%%frameptr
%endif

%endif

%define _basedir           /usr
%define _subdir            
%define _prefix		   %{_basedir}
%define _sysconfdir	   /etc
%define _localedir	   %{_libdir}/locale
%define _localstatedir     /var
%define _pkg_config_path   %{_libdir}/pkgconfig
%define _pkg_config_path64 %{_libdir}/%{_arch64}/pkgconfig

# ChangeLog:
#
# 2006-06-18  Laszlo Peter  <laca@sun.com>
# - review and update for spec-files-extra
# 2006-06-02  Laszlo Peter  <laca@sun.com>
# - add the date string back into REV
# 2005-11-28  Laszlo Peter  <laca@sun.com>
# - add -z combreloc and -Bdirect to the LDFLAGS
# 2005-10-23  Laszlo Peter  <laca@sun.com>
# - define debug_build (if --with-debug is used) and build_l10n
#   (when --with-l10n is used)  build_l10n will disable building
#   the l10n packages but needs changes in the spec files to work;
#   debug_build is already functional: replaces the optimisation flags
#   with -g and disables stripping the binaries. (Yay!)
# 2005-10-14  Laszlo Peter  <laca@sun.com>
# - define _ldflags
# 2005-09-19  Laszlo Peter  <laca@sun.com>
# - add -xregs=no%frameptr (Sun CC) or -fomit-frame-pointers (gcc)
#   flags to enable dtrace get stack traces
# 2005-09-17  Laszlo Peter  <laca@sum.com>
# - define %picflags and add them to the gcc CFLAGS otherwise most things
#   seem to break
# 2005-09-16  Laszlo Peter  <laca@sun.com>
# - define cc_is_gcc and define gcc specific compiler flags
# 2005-09-15  Brian Cameron  <brian.cameron@sun.com>
# - Backout debug lines I accidently committed to this file.
# 2005-07-14  Laszlo Peter  <laca@sun.com>
# - update product version to 2.10
# 2004-11-01  Laszlo Peter  <laca@sun.com>
# - temporarily removed -O for amd64 to stop gtk-demo crashing
# 2004-10-13  Laszlo Peter  <laca@sun.com>
# - defined _pkg_config_path64
# 2004-10-02  Laszlo Peter  <laca@sun.com>
# - defined jds_version
# 2004-10-02  Joseph Townsend <jan@eng.sun.com>
# - Create 64bit libraries for Solaris
# 2004-08-12  Shirley Woo  <shirley.woo@sun.com>
# - Updated SUNW_Category for G2.6 packages to 2.6.0
# 2004-07-23  Laszlo Peter  <laca@sun.com>
# - Changed default copyright notice to default-copyright.txt
# - Prefixed REV with 9.7.2
# 2004-06-26  Shirley Woo  <shirley.woo@sun.com>
# - Changed install location to /usr/...
# 2004-06-21  Laszlo Peter  <laca@sun.com>
# - descrease C++ optimisation level to xO3
# - define _pkg_config_path
# 2004-05-03  Laszlo Peter  <laca@sun.com>
# - define _basedir
# 2004-04-14  Laszlo Peter  <laca@sun.com>
# - change CATEGORY to GNOME2,application,JDS3
# 2004-02-28  Laszlo Peter  <laca@sun.com>
# - add -mr and -xtrconst options, -xpentium on intel.
# - define cxx_optflags for CC compilation
