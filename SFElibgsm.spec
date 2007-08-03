#
# spec file for package SFElibgsm
#
# includes module(s): libgsm
#
%include Solaris.inc

%define	src_ver 1.0.12
%define	src_name libgsm
%define	src_url	http://kbs.cs.tu-berlin.de/~jutta/gsm/gsm-%{version}.tar.gz

Name:		SFElibgsm
Summary:	GSM audio encoding/decoding library
Version:	%{src_ver}
License:	Free (Copyright (C) Technische Universitaet Berlin)
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libgsm-01-makefile.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This is a free and public implementation of GSM audio encoding and
decoding. The gsm library is used in many free software projects
including 'rplay', but has never been packaged as a stand-alone shared
library. GSM encoding has specific uses in transmission of packetized
audio over the Internet.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n gsm-1.0-pl12
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

rm -f bin/* lib/* shared/* src/*.o test/*.o

export PICFLAG="-KPIC"
export OPTFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{1,3},%{_includedir},%{_libdir}}
make install DESTDIR=$RPM_BUILD_ROOT INSTALL_ROOT=%{_prefix}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man3

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
