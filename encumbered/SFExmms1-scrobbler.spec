#
# spec file for package SFExmms1-scrobbler
#
# includes module(s): xmms1-scrobbler
#

%include Solaris.inc

Name:                SFExmms1-scrobbler
Summary:             XMMS Scrobbler is a plugin for xmms that reports your music listening to last.fm.
Version:             0.4.0
Source:              http://xmms-scrobbler.sommitrealweird.co.uk/download/xmms-scrobbler-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

Requires: %name
Requires: SUNWopenssl-libraries
Requires: SFExmms1
Requires: SFElibmusicbrainz3
Requires: SFEtaglib
BuildRequires: SFEtaglib-devel
BuildRequires: SFExmms1-devel

%prep
%setup -q -n xmms-scrobbler-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

./configure \
        --prefix=%{_prefix} \
        --disable-bmp-plugin
        
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/xmms/General/libxmms_scrobbler.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/xmms/General/


%changelog
* Thu May 1 - andras.barna@gmail.com
- Initial spec.
