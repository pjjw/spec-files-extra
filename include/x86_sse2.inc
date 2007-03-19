#
# Intel SSE2 ISA settings for Solaris packages
#
# Copyright 2007 Sun Microsystems, Inc.
#
# Solaris.inc must be included before this file

%define bld_arch	pentium_pro+mmx
%define sse2_arch       pentium_pro+mmx

%define opt_sse2 1
%define can_isaexec 1
%define gtk_doc_option --disable-gtk-doc

%define arch_ldadd           -xarch=sse2 -L%{_libdir} -R%{_libdir}

%if %debug_build
%define pkgbuild_postprocess /bin/true
%define _cc_opt_level      -g
%define _cxx_opt_level     -g
%define _gcc_opt_level     -g
%define _gxx_opt_level     -g
%else
%if %cc_is_gcc
%define _gcc_opt_level     -O3
%define _gxx_opt_level     -O3
%else
%define _cc_opt_level      -xO4 -xspace
%define _cxx_opt_level     -xO3 -xspace
%endif
%endif

%define gcc_optflags           %_gcc_opt_level -mcpu=pentiumpro -mtune=pentiumpro -msse2 -Xlinker -i -fno-omit-frame-pointer %gcc_picflags
%define gcc_cxx_optflags       %_gxx_opt_level -mcpu=pentiumpro -mtune=pentiumpro -msse2 -Xlinker -i -fno-omit-frame-pointer %gcc_picflags

%define suncc_optflags           -i %_cc_opt_level -xstrconst -xarch=sse2 -xvector -mr -xregs=no%%frameptr
%define suncc_cxx_optflags       -i %_cxx_opt_level -xarch=sse2 -xvector -mr -norunpath -xregs=no%%frameptr

%if %cc_is_gcc

%define picflags %gcc_picflags
%define optflags %gcc_optflags
%define cxx_optflags %gcc_cxx_optflags

%else
# cc is not gcc

%define picflags %suncc_picflags
%define optflags %suncc_optflags ${EXTRA_CFLAGS}
%define cxx_optflags %suncc_cxx_optflags ${EXTRA_CXXFLAGS}

%endif

%define _bindir		 %{_prefix}/bin/%{bld_arch}
%define _libdir		 %{_prefix}/lib/%{bld_arch}
%define _libexecdir	 %{_prefix}/lib/%{bld_arch}
%define _pkg_config_path %{_libdir}/%{bld_arch}/pkgconfig

# ChangeLog:
# 2007-03-19  Doug Scott  <dougs@truemail.co.th>
# - Fixed -fno-omit-frame-pointer flag
# 2007-03-15  Laszlo (Laca) Peter  <laca@sun.com>
# - define suncc_optflags, suncc_cxx_optflags, gcc_optflags, gcc_cxx_optflags
# 2007-03-12  Doug Scott <dougs@truemail.co.th>
