#
# spec file for package SFEdillo.spec
#
# includes module(s): dillo
#
%include Solaris.inc

%define src_name	dillo
%define src_url		http://www.dillo.org/download

Name:                   SFEdillo
Summary:                Lightweight browser
Version:                0.8.6
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#Requires:	SUNWGtku

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

libtoolize --force

export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -Lusr/sfw/lib -Rusr/sfw/lib"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --disable-dlgui		\
	    --disable-gtktest

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Remove SUNWGtku (gtk 1.x) dependency to get module to build.
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
