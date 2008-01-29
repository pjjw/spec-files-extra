%include Solaris.inc

%define src_name espeak
%define src_url http://kent.dl.sourceforge.net/sourceforge/%{src_name}

Name:		SFEespeak
Summary:	eSpeak - compact open source software speech synthesizer
Version:	1.31
Source:		%{src_url}/%{src_name}-%{version}-source.zip
Patch1:		espeak-01-solaris.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEpulseaudio-devel
Requires: SFEpulseaudio

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}-source
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
cd src
make -j$CPUS CXX=gcc SONAME_OPT=-Wl,-h, EXTRA_LIBS=-lm

%install
rm -rf $RPM_BUILD_ROOT
cd src
make install DESTDIR=$RPM_BUILD_ROOT CXX=gcc SONAME_OPT=-Wl,-h, EXTRA_LIBS=-lm
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Tue Jan 29 2008 - Willie Walker
- Initial spec

