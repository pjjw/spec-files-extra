#
# spec file for package SFEunrar
#
# includes module(s): unrar
#
%include Solaris.inc

Name:                    SFEunrar
Summary:                 Unrar Decompressor
Version:                 3.5.4
Source:                  http://www.rarlab.com/rar/unrarsrc-%{version}.tar.gz
URL:                     http://www.rarlab.com/
Patch1:			 unrar.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWlibms

%prep
%setup -q -n unrar
%patch1 -p1
touch NEWS
touch AUTHORS

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP -DSOLARIS"
export CXXFLAGS="%cxx_optflags -I/usr/sfw/include -DANSICPP -DSOLARIS -D`uname -m`"
export RPM_OPT_FLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export STRIP=/usr/ccs/bin/strip

make -f makefile.unix -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make -f makefile.unix BASENAME=${RPM_BUILD_ROOT}%{_prefix}	\
     MANDIR=${RPM_BUILD_ROOT}%{_mandir} DESTDIR=$RPM_BUILD_ROOT INSTALL=install install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Thu Jun 22 2006 - laca@sun.com
- rename to SFEunrar
- add missing deps
- move to /usr/bin
* Fri May 12 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
