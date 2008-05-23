#
# spec file for package SUNWfaad2.spec
#
# includes module(s): faad2
#
%include Solaris.inc

Name:                    SFEfaad2
Summary:                 faad2 - a high-quality MPEG audio decoder
Group:                   libraries/multimedia
Version:                 2.6.1
Source:                  %{sf_download}/faac/faad2-%{version}.tar.gz
URL:                     http://www.audiocoding.com/
#Patch1:                  faad-01-makefile.diff
Patch2:                  faad-02-inline.diff
#Patch3:                  faad-03-largefiles.diff
Patch4:                  faad-04-wall.diff
#Patch5:                  faad-05-strchr.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWid3lib
BuildRequires: SUNWid3lib-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n faad2
#%patch1 -p1
%patch2 -p1
#%patch3 -p1
%patch4 -p1
#%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# Compiler bug forces us back to -xO2 for the moment
#export CFLAGS="`echo "%optflags" | sed 's/-xO4/-xO2/'`"
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
%ifarch sparc
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

autoreconf --install
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-mp4v2                     \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- id3 is now part of nevada so dependencies should point to SUNWid3 and SUNWid3-devel, thanks to Giles Dauphin for the fix
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 2.6.1.  Bump patch2 and patch4.  Comment patch1, patch3 and patch5.
* Fri Jun 23 2005 - laca@sun.com
- rename to SFEfaad2
- update file attributes
- remove lib*a
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
