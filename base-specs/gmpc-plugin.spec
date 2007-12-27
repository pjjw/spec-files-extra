#
# base-spec file for package SFEgmpc-plugin-**** (plugin)
#
# use gcc to compile
#

%define gmpcmainversion 0.15.5

Name:			gmpc-plugin-%{pluginname}
URL:                     http://sarine.nl/gmpc
Version:                 0.15.5.0
#Source:                  http://download.sarine.nl/gmpc-%{gmpcmainversion}/plugins/gmpc-%{pluginname}-%{version}.tar.gz
Source:			 http://download.qballcow.nl/gmpc-%{gmpcmainversion}/gmpc-%{pluginname}-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires:           SFEgmpc-devel
Requires:                SFEgmpc

%include default-depend.inc

%prep
%setup -q -n gmpc-%{pluginname}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export LDFLAGS="-lX11"
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

CC=/usr/sfw/bin/gcc CXX=/usr/sfw/bin/g++ ./configure --prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir}              \
	--libexecdir=%{_libexecdir}      \
	--sysconfdir=%{_sysconfdir}

  

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/gmpc/plugins/*.la
find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gmpc
%dir %attr (0755, root, other) %{_datadir}/gmpc/plugins
%{_datadir}/gmpc/plugins/*.so


%changelog
* Sun Dec 02 2007 - Thomas Wagner
- initial base-spec for gmpc-plugin
