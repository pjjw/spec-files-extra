%include Solaris.inc

%define src_name espeak
%define src_url http://kent.dl.sourceforge.net/sourceforge/%{src_name}
%define with_pulseaudio %(pkginfo -q SFEpulseaudio && echo 1 || echo 0)
%define with_portaudio %(pkginfo -q SFEportaudio && echo 1 || echo 0)


Name:		SFEespeak
Summary:	eSpeak - compact open source software speech synthesizer
Version:	1.31
Source:		%{src_url}/%{src_name}-%{version}-source.zip
Patch1:		espeak-01-makefile.diff
Patch2:		espeak-02-pulseaudio.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# If neither PulseAudio or PortAudio is installed, then depend on
# PulseAudio, since it works with SADA and PortAudio does not.
#
%if %with_pulseaudio
%else
%if %with_portaudio
%else
BuildRequires: SFEpulseaudio-devel
Requires: SFEpulseaudio
%endif
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}-source
%patch1 -p1

# If building with PulseAudio, add patch to configure building with
# PulseAudio
#
%if %with_pulseaudio
%patch2 -p1
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
cd src

# Set up PortAudio header file to use version 1.9.  If
# building with PulseAudio, this file is ignored.
#
cp %{_builddir}/espeak-%version-source/src/portaudio19.h %{_builddir}/espeak-%version-source/src/portaudio.h

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd src
make install DESTDIR=$RPM_BUILD_ROOT
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

