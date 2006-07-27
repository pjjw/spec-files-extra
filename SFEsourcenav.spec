#
# spec file for package SFEsourcenav
#
# includes module(s): sourcenav
#
%include Solaris.inc

Name:                    SFEsourcenav
Summary:                 sourcenav - source code analysis tool
Version:                 5.2
%define tarball_version  5.2b2
Source:                  http://kent.dl.sourceforge.net/sourceforge/sourcenav/sourcenav-%{tarball_version}.tar.gz
URL:                     http://sourcenav.sourceforge.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n sourcenav-%{tarball_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -DANSICPP"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --datadir=%{_datadir}/sourcenav     \
	    --libdir=%{_libdir}			\
	    --libexecdir=%{_libexecdir}		\
	    --sysconfdir=%{_sysconfdir}
	    
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
mv man/mann/* $RPM_BUILD_ROOT/%{_mandir}/mann/
rm -rf man
rm -rf COPYING INSTALL.TXT NEWS README.TXT html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/sourcenav/bitmaps
%{_datadir}/sourcenav/demos
%{_datadir}/sourcenav/etc
%{_datadir}/sourcenav/itc*
%{_datadir}/sourcenav/itk*
%{_datadir}/sourcenav/redhat
%{_datadir}/sourcenav/sdk
%{_datadir}/sourcenav/sourcenav
%{_datadir}/sourcenav/tcl*
%{_datadir}/sourcenav/tix*
%{_datadir}/sourcenav/tk*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Jul 23 2006 - laca@sun.com
- rename to SFEsourcenav
- mv datadir stuff into datadir/sourcenav subdir
- define tarball_version because Version should not include letters
- define -devel subpkg
* Mon Jul 17 2006 - Halton Huo <halton.huo@sun.com>
- Initial spec.

