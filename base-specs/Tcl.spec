#
# spec file for package libraw1394
#
# includes module(s): libraw1394
#

%define src_ver 8.4.15
%define src_name tcl
%define src_url http://jaist.dl.sourceforge.net/sourceforge/tcl

Name:		Tcl
Summary:	Tool Command Language embeddable scripting language
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}%{src_ver}-src.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{src_ver}-build

%prep
%setup -q -n %{src_name}%{src_ver}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd unix 

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize -f -c
aclocal
autoconf -f

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static

#perl -pi -e 's/-shared/-Wl,-G/' libtool
make

%install
cd unix
make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Sep 22 2007 - dougs@truemail.co.th
- Initial base spec file
