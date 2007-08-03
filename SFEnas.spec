#
# spec file for package SFEnas
#
# includes module(s): nas
#
%include Solaris.inc

%define	src_ver 1.9
%define	src_name nas
%define	src_url	http://nas.codebrilliance.com/nas

%define openwin		/usr/openwin
%define openwinlib	%{openwin}/lib
%define openwinbin	%{openwin}/bin
%define openwindata	%{openwin}/share
%define openwininclude	%{openwin}/include

Name:		SFEnas
Summary:	Network Audio System
Version:	%{src_ver}
License:	Free
Source:		%{src_url}/%{src_name}-%{version}.src.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package contains a network-transparent, client/server audio
system, with a library. Key features of the Network Audio System
include:
 - Device-independent audio over the network
 - Lots of audio file and data formats
 - Can store sounds in server for rapid replay
 - Extensive mixing, separating, and manipulation of audio data
 - Simultaneous use of audio devices by multiple applications
 - Use by a growing number of ISVs
 - Small size
 - Free! No obnoxious licensing terms.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lX11"

xmkmf
make World

%install

rm -rf $RPM_BUILD_ROOT
make install install.man 	\
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{openwinlib}/lib*.*a
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{openwinlib}/lib*.so* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{openwinbin} $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{openwininclude} $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT%{openwindata} $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{openwin}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
