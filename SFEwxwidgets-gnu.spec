#
# spec file for package SFEwxwidgets-spp
#
# includes module(s): wxWidgets
#

%include Solaris.inc
%include usr-gnu.inc

Name:                    SFEwxwidgets-gnu
Summary:                 wxWidgets - Cross-Platform GUI Library (g++)
URL:                     http://wxwidgets.org/
Version:                 2.8.4
%define tarball_version  2.8.4
Source:			 http://easynews.dl.sourceforge.net/sourceforge/wxwindows/wxWidgets-%{tarball_version}.tar.bz2
Patch1:                  wxwidgets-01-msgfmt.diff
Patch2:                 wxwidgets-02-sqrt.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-libs

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
%setup -q -n wxWidgets-%tarball_version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPPFLAGS="-I/usr/X11/include"
export CC=gcc
export CFLAGS="%{gcc_optflags}"
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export LDFLAGS="%{_ldflags} -lm"
export LD_OPTIONS="-i -L%{_libdir} -L/usr/X11/lib -R%{_libdir}:/usr/X11/lib"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}			\
	    --with-gtk				\
	    --enable-gtk2			\
            --enable-unicode			\
            --enable-mimetype                   \
            --with-sdl                          \
            --without-expat                     \
            --with-gnomeprint

make -j$CPUS
cd contrib
make -j$CPUS
cd ..
cd locale
make allmo
cd ..

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd contrib
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

cd $RPM_BUILD_ROOT%{_bindir}
rm -f wx-config
ln -s ../lib/wx/config/gtk2-unicode-release-* wx-config

%if %build_l10n
# Rename zh dir to zh_CN as zh is a symlink to zh_CN and causing installation
# problems as a dir.
cd $RPM_BUILD_ROOT%{_datadir}/locale
mv zh zh_CN
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

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
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/bakefile
%dir %attr(0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/bakefile/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Aug 11 2007 - trisk@acm.jhu.edu
- Bump to 2.8.4 for compatibility with SFEwxwidgets
- Use CC=gcc to be consistent and not confuse build system
* Sat Jul 14 2007 - dougs@truemail.co.th
- Converted from SFEwxwidgets.spec
