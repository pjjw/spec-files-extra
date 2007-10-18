#
# spec file for package SFEmpgtx
#
# includes module(s): SFEmpgtx
#
%include Solaris.inc

Name:                    SFEmpgtx
Summary:                 MPEG file toolbox, that slices and joins audio and video files
Version:                 1.3
Source:                  http://nchc.dl.sourceforge.net/sourceforge/mpgtx/mpgtx-%{version}.tgz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC

%prep
%setup -q -n mpgtx-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
%ifarch sparc
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

export CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include"

${CXX}  ${CXXFLAGS} -DNOSIGNAL_H -o mpgtx *.cxx

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp mpgtx $RPM_BUILD_ROOT/usr/bin
( 
  cd $RPM_BUILD_ROOT/usr/bin 
  ln -s mpgtx mpgjoin
  ln -s mpgtx mpgsplit
  ln -s mpgtx mpgcat
  ln -s mpgtx mpginfo
  ln -s mpgtx mpgdemux
  ln -s mpgtx tagmp3
)
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
cp man/mpgtx.1 $RPM_BUILD_ROOT/usr/share/man/man1
cp man/mpgtx.1 $RPM_BUILD_ROOT/usr/share/man/man1/mpgjoin
cp man/mpgtx.1 $RPM_BUILD_ROOT/usr/share/man/man1/mpgsplit
cp man/mpgtx.1 $RPM_BUILD_ROOT/usr/share/man/man1/mpgcat
cp man/mpgtx.1 $RPM_BUILD_ROOT/usr/share/man/man1/mpginfo
cp man/mpgtx.1 $RPM_BUILD_ROOT/usr/share/man/man1/mpgdemux
cp man/tagmp3.1 $RPM_BUILD_ROOT/usr/share/man/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
