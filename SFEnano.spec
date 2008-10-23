#
# spec file for package SFEnano
#
# includes module(s): nano
#

%include Solaris.inc

Name:                    SFEnano
Summary:                 GNU nano text editor
Version:                 2.0.9
Source:			 http://www.nano-editor.org/dist/v2.0/nano-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEncursesw

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


%prep
rm -rf %name-%version
%setup -q -n nano-%version

%build
export CFLAGS="%optflags -I/usr/gnu/include -I/usr/gnu/include/ncursesw"
export CPPFLAGS="%optflags -I/usr/gnu/include -I/usr/gnu/include/ncursesw"
export LDFLAGS="%{_ldflags} -R/usr/gnu/lib -L/usr/gnu/lib -lncursesw"
./configure --prefix=%{_prefix}			\
                 --bindir=%{_bindir}			\
                 --mandir=%{_mandir}                 \
                 --infodir=%{_infodir}                   \
                 --enable-all

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_mandir}/fr
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_infodir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/nano
%{_datadir}/nano/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Oct 23 2008 - andras.barna@gmail.com
- new version, add --enable-all, add SFEncursesw for utf-8
* Wed Jul  5 2006 - laca@sun.com
- rename to SFEnano
- delete -share subpkg
- update file attributes
* Fri Feb  3 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec

