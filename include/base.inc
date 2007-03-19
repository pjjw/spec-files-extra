#
# Base (32-bit) platform settings for Solaris packages
#
# Copyright 2007 Sun Microsystems, Inc.
#
# Solaris.inc must be included before this file

%ifarch sparc
%define bld_arch        "sparc"
%else
%define bld_arch	"i386"
%endif

# use --without-gtk-doc to disable building gtk-docs (it takes quite
# a while to build them)
# default: build gtk-doc API docs
%define gtk_doc_option %{?!_without_gtk_doc:--enable-gtk-doc}%{?_without_gtk_doc:--disable-gtk-doc}

%define arch_ldadd

%if %debug_build
%define pkgbuild_postprocess /bin/true
%define _cc_opt_level      -g
%define _cxx_opt_level     -g
%define _gcc_opt_level      -g
%define _gxx_opt_level     -g
%else
%if %cc_is_gcc
%define _gcc_opt_level      -O3
%define _gxx_opt_level     -O3
%else
%define _cc_opt_level      -xO4 -xspace
%define _cxx_opt_level     -xO3 -xspace
%endif
%endif

%ifarch sparc
%define gcc_optflags           %_gcc_opt_level -mv8plus -Xlinker -i %gcc_picflags
%define gcc_cxx_optflags       %_gxx_opt_level -mv8plus -Xlinker -i %gcc_picflags
%endif

%ifarch i386
%define gcc_optflags           %_gcc_opt_level -march=i586 -Xlinker -i -fno-omit-frame-pointer %gcc_picflags
%define gcc_cxx_optflags       %_gxx_opt_level -march=i586 -Xlinker -i -fno-omit-frame-pointer %gcc_picflags
%endif

%ifarch sparc
%define suncc_optflags           -i %_cc_opt_level -xstrconst -xarch=v8a -mr
%define suncc_cxx_optflags       -i %_cxx_opt_level -xarch=v8a -mr -norunpath
%endif

%ifarch i386
%define suncc_optflags           -i %_cc_opt_level -xstrconst -xpentium -mr -xregs=no%%frameptr
%define suncc_cxx_optflags       -i %_cxx_opt_level -pentium -mr -norunpath -xregs=no%%frameptr
%endif

%if %cc_is_gcc

%define picflags %gcc_picflags
%define optflags %gcc_optflags
%define cxx_optflags %gcc_cxx_optflags

%else
# cc is not gcc

%define picflags %suncc_picflags
%define optflags %suncc_optflags ${EXTRA_CFLAGS}
%define cxx_optflags %suncc_cxx_optflags ${EXTRA_LDFLAGS}

%endif

%define _bindir		 %{_prefix}/bin
%define _libdir		 %{_prefix}/lib
%define _libexecdir	 %{_prefix}/lib
%define _pkg_config_path %{_libdir}/pkgconfig
%define _sysconfdir      /etc

# ChangeLog:
# 2007-03-19  Doug Scott  <dougs@truemail.co.th>
# - Fixed -fno-omit-frame-pointer flag
# 2007-03-15  Laszlo (Laca) Peter  <laca@sun.com>
# - copied from x86_sse2.inc
# - new include file that resets macros to their default (32-bit build)
#   values
# 2007-03-12  Doug Scott  <dougs@truemail.co.th>
