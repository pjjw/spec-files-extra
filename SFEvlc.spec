#
# spec file for package SFEvlc
#
# includes module(s): vlc
#
%include Solaris.inc

Name:                    SFEvlc
Summary:                 vlc - the cross-platform media player and streaming server
Version:                 0.8.6a
Source:                  http://download.videolan.org/pub/videolan/vlc/0.8.6a/vlc-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWhal
Requires: SUNWdbus
Requires: SFElibdvbpsi
Requires: SUNWlibcdio
BuildRequires: SUNWdbus-devel
BuildRequires: SFElibdvbpsi-devel
BuildRequires: SUNWlibcdio-devel


%prep
%setup -q -n vlc-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%changelog
* Thu Mar 22 2007 - daymobrew@users.sourceforge.net
- Initial version
