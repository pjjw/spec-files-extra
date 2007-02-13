#
# spec file for package SFExmlto
#
# includes module(s): xmlto
#

%include Solaris.inc

Name:                    SFExmlto
Summary:                 xmlto - converts an XML file into a specified format
Version:                 0.0.18
Source:                  http://cyberelk.net/tim/data/xmlto/stable/xmlto-%{version}.tar.bz2
URL:			 http://directory.fsf.org/all/xmlto.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlxsl
Requires: SUNWgnome-xml-share
Requires: SFEgetopt
Requires: SFEfindutils

%prep
rm -rf %name-%version
%setup -q -n xmlto-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export GETOPT=/usr/gnu/bin/getopt
export FIND=/usr/gnu/bin/find
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}/xmlto/xsl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/xmlto
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue Feb 13 2007 - laca@sun.com
- create
