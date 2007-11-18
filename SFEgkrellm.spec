#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define SUNWgnugettext      %(/usr/bin/pkginfo -q SUNWgnu-gettext && echo 1 || echo 0)

Name:                SFEgkrellm
Summary:             Popular (ubiquitous) Gtk-based system monitor
Version:             2.2.10
Source:              http://members.dslextreme.com/users/billw/gkrellm/gkrellm-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SUNWgnugettext
BuildRequires: SUNWgnu-gettext-devel
Requires: SUNWgnu-gettext
%else
BuildRequires: SFEgettext-devel
Requires: SFEgettext
%endif

# Guarantee X/GTK/freetype environment, concisely (hopefully)
BuildRequires: SUNWGtku
# The above causes many things to get pulled in
BuildRequires: SUNWxwplt 
# The above brings in many things, including SUNWxwice and SUNWzlib
BuildRequires: SUNWxwxft 
# The above also pulls in SUNWfreetype2

Requires: SUNWGtku
Requires: SUNWxwplt 
Requires: SUNWxwxft 
Requires: SUNWlexpt
Requires: SUNWmlib
Requires: SUNWpng

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n gkrellm-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CC=/usr/sfw/bin/gcc
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export LD_OPTIONS="-L/usr/sfw/lib -R/usr/sfw/lib"

# A couple patches follow. TODO: Transpose these into proper patches or
# (better yet) report them upstream.
#
# The following patches src/configure to explicitely use /bin/bash, not
# /bin/sh because bash-specific syntax is what the script actually requires:

perl -i.orig -lpe 'if ($. == 1){s/^.*$/#!\/bin\/bash/}' src/configure

# Another patch:
perl -i.orig -lpe 'if ($. == 21){print "
#define u_int8_t uint8_t
#define u_int16_t uint16_t
#define u_int32_t uint32_t
#define u_int64_t uint64_t
"}' server/main.c

# Apparently msgfmt usage in this source is GNU-specific, so 
# the following forces GNU msgfmt to be used:
export PATH=/usr/gnu/bin:$PATH

make -j$CPUS solaris

%install
rm -rf $RPM_BUILD_ROOT

install -D src/gkrellm $RPM_BUILD_ROOT%{_bindir}/gkrellm
install -D gkrellm.1   $RPM_BUILD_ROOT%{_mandir}/man1/gkrellm.1

install -D gkrellm.pc  $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gkrellm.pc

install -d $RPM_BUILD_ROOT%{_includedir}/gkrellm2
install src/gkrellm.h src/gkrellm-public-proto.h \
           $RPM_BUILD_ROOT%{_includedir}/gkrellm2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gkrellm
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/gkrellm.1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_includedir}/gkrellm2
%{_includedir}/gkrellm2/gkrellm*.h
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/gkrellm.pc

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWgnu-gettext or SFEgettext.
* Fri Apr 20 2007 - dougs@truemail.co.th
- Added SFW libs (LDFLAGS,LD_OPTIONS)
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Mar 11 2007 - Eric Boutilier
- Initial spec
