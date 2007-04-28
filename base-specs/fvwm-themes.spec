#
# spec file for package fvwm.spec
#
# includes module(s): fvwm
#
%include Solaris.inc

%define src_url		http://prdownloads.sourceforge.net/fvwm-themes

Name:                   fvwm-themes
Summary:                fvwm themes
Version:                0.7.0
Source:                 %{src_url}/%{name}-%{version}.tar.bz2
Source1:                %{src_url}/%{name}-extra-%{version}.tar.bz2
Patch1:			fvwm-themes-01-postrun.diff
Patch2:			fvwm-themes-02-xlsfonts.diff
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -b1 -n %{name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/X11/include -I$PWD/fvwm-%{fvwm.version}"
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags} -L/usr/X11/lib -R/usr/X11/lib"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
automake --add-missing
autoconf --force

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
            --enable-shared			\
	    --disable-static		

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
cd ../%{name}-extra-%{version}
cp -pr * $RPM_BUILD_ROOT%{_datadir}/fvwm/themes

%changelog
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
