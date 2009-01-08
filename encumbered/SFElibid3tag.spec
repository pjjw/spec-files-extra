#
# spec file for package SFElibid3tag
#
# includes module(s): libid3tag
#

%include Solaris.inc

Name:         SFElibid3tag
Summary:      libid3tag
License:      GPL
Group:        System/GUI/GNOME
Version:      0.15.1.2
%define tarball_version 0.15.1b
Release:      1
Source:       %{sf_download}/mad/libid3tag-%{tarball_version}.tar.gz
Patch1:		  libid3tag-01-a_capella.patch
Patch2:		  libid3tag-02-utf16.patch
Patch3:		  libid3tag-03-unknown_encoding.patch
URL:          http://www.underbit.com/products/mad/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%name-%{version}-build
%include default-depend.inc
Requires:     SUNWzlib

%description
ID3 tag manipulation library a wide range of multimedia formats

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-libs

%prep
%setup -q -n libid3tag-%{tarball_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"

touch NEWS
touch AUTHORS
touch ChangeLog
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir}         \
        --bindir=%{_bindir}         \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir}         \
        --localstatedir=/var/lib
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{tarball_version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Jan  8 2009 - Peter Woodman <peter@shortbus.org>
- adding debian's patches to correct utf16 and unknown encoding handling errors
* Wed Jul  5 2006 - laca@sun.com
- rename to SFElibid3tag
- delete unnecessary env variables and dependencies
* Thu Apr  6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Thu Mar 16 2006 - damien.carbery@sun.com
- Correct URL and version.
* Thu Mar 09 2006 - brian.cameron@sun.com
- Created,  
