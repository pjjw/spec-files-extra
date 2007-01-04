#
# spec file for package SFEdvdauthor
#
# includes module(s): SFEdvdauthor
#
%include Solaris.inc

Name:                    SFEdvdauthor
Summary:                 dvdauthor a program that will generate a DVD movie
Version:                 0.6.11
Source:                  http://nchc.dl.sourceforge.net/sourceforge/dvdauthor/dvdauthor-%{version}.tar.gz
Patch1:			 dvdauthor-01-types.diff
Patch2:			 dvdauthor-02-wall.diff
Patch3:			 dvdauthor-03-typo.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SFElibdvdread
BuildRequires: SFElibdvdread-devel

%prep
%setup -q -n dvdauthor-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

LDFLAGS="-L/usr/X11/lib -L/usr/sfw/lib -R/usr/X11/lib:/usr/sfw/lib" \
CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include" \
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_bindir}/*
%{_datadir}/*

%changelog
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
