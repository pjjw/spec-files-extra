#
# spec file for package SFEgpac
#
# includes module(s): gpac
#
%include Solaris.inc

%define	src_name gpac

Name:                SFEgpac
Summary:             Open Source multimedia framework
Version:             0.4.4
URL:                 http://gpac.sourceforge.net/
Source:              http://%{sf_mirror}/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		     gpac-new-01.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEfreeglut-devel
Requires: SFEfreeglut
BuildRequires: SFElibmad-devel
Requires: SFElibmad
BuildRequires: SFEfaad2-devel
Requires: SFEfaad2
Requires: SUNWfreetype2
#BuildRequires: SFEwxwidgets-gnu-devel
#Requires: SFEwxwidgets-gnu
BuildRequires: SFEwxwidgets-devel
Requires: SFEwxwidgets

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
unset P4PORT
%setup -q -n gpac
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export PATH=/usr/gnu/bin:$PATH
export LDFLAGS="%_ldflags"
#export LD_OPTIONS="-i -L/usr/gnu/lib -L/usr/X11/lib -R/usr/gnu/lib:/usr/X11/lib:/usr/sfw/lib"
#export CXX=g++
export CXX=CC
#RPM_OPT_FLAGS="-O4 -fPIC -DPIC -fno-omit-frame-pointer"
RPM_OPT_FLAGS="-KPIC -DPIC "

chmod 755 ./configure
./configure --prefix=%{_prefix}		\
            --mandir=%{_mandir}		\
	    --cc=cc			\
	    --extra-ldflags="-KPIC"	\
	    --extra-libs="-lrt -lm"	\
	    --disable-opt		\
	    --mozdir=/usr/lib/firefox	\
	    --extra-cflags="$RPM_OPT_FLAGS"
echo "CXX=CC" >> config.mak
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
%dir %attr (0755, root, bin) %{_mandir}
%{_datadir}/gpac
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Nov 21 2008 - dauphin@enst.fr
- gpac with Studio12 and new freeglut
- TODO: check ffmepg option (build with)
* Tue Sep 02 2008 - halton.huo@sun.com
- s/SFEfreetype/SUNWfreetype2
* Thu Jun 19 2008 - river@wikimedia.org
- need to unset P4PORT during %setup or gpatch behaves oddly
* Fri May 23 2008 - michal.bielicki@voiceworks.pl
- rights change for mandir, fix by Giles Dauphin
* Mon Dec 31 6 2007 - markwright@internode.on.net
- Add patch 4 to fix trivial compiler error missing INADDR_NONE.
- Add --extra-libs="-lrt -lm".
* Mon Jul 30 2007 - dougs@truemail.co.th
- Install headers
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
