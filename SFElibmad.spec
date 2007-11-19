#
# spec file for package SFElibmad 
#

%include Solaris.inc
Name:                    SFElibmad
Summary:                 libmad - High-quality MPEG audio decoder
URL:                     http://www.underbit.com/products/mad/
Version:                 0.15.1b
Source:                  ftp://ftp.mars.org/pub/mpeg/libmad-0.15.1b.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}


%prep
%setup -q -n libmad-%version

%build
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl -lsocket"
%endif
export LDFLAGS="-lX11"

./configure --prefix=%{_prefix} --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libmad.a
rm $RPM_BUILD_ROOT%{_libdir}/libmad.la

%if %{build_l10n}
%else
rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Mon Nov 19 2007 - daymobrew@users.sourceforge.net
- Initial version.
