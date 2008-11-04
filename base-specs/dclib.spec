#
# spec file for package dclib
#

Name:		dclib
Summary:	Library for the Direct Connect network.
Version:	0.3.21
Source:		%{sf_download}/wxdcgui/%{name}-%{version}.tar.bz2
Patch1:         valknut-01-sockio.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

autoreconf --verbose --install

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Nov 4 2008 - Andras Barna (andras.barna@gmail.com)
- Initial spec file

