#
# spec file for package SFEgpac
#
# includes module(s): gpac
#
%include Solaris.inc

%define	src_name gpac
%define	src_url	http://downloads.sourceforge.net/gpac

Name:                SFEgpac
Summary:             Open Source multimedia framework
Version:             0.4.4
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     gpac-01-libs.diff
Patch2:		     gpac-02-gcc.diff
Patch3:		     gpac-03-install.diff
Patch4:		     gpac-04-inaddr.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEfreeglut-devel
Requires: SFEfreeglut
BuildRequires: SFElibmad-devel
Requires: SFElibmad
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
BuildRequires: SFEfreetype-devel
Requires: SFEfreetype
BuildRequires: SFEwxwidgets-gnu-devel
Requires: SFEwxwidgets-gnu

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n gpac
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=/usr/gnu/bin:$PATH
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-i -L/usr/gnu/lib -L/usr/X11/lib -R/usr/gnu/lib:/usr/X11/lib:/usr/sfw/lib"
export CXX=g++
RPM_OPT_FLAGS="-O4 -fPIC -DPIC -fno-omit-frame-pointer"

chmod 755 ./configure
./configure --prefix=%{_prefix}		\
            --mandir=%{_mandir}		\
	    --cc=gcc			\
	    --extra-ldflags="-fPIC"	\
	    --extra-libs="-lrt -lm"	\
	    --disable-opt		\
	    --mozdir=/usr/lib/firefox	\
	    --extra-cflags="$RPM_OPT_FLAGS"
echo "CXX=g++" >> config.mak
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/gpac
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gpac
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%changelog
* Mon Dec 31 6 2007 - markwright@internode.on.net
- Add patch 4 to fix trivial compiler error missing INADDR_NONE.
- Add --extra-libs="-lrt -lm".
* Mon Jul 30 2007 - dougs@truemail.co.th
- Install headers
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
