#
# spec file for package SFEgtodo2
#
# use gcc to compile

%include Solaris.inc
Name:                    SFEgtodo2
Summary:                 gtodo2 - A gnome Task-List-Manager
URL:                     http://sarine.nl/gnome-task-list-manager
Version:                 0.19.0
#TODO#   remove -beta 
Source:                  http://download.sarine.nl/gtodo2/gtodo2-%{version}-beta.tar.gz

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc


%prep
%setup -q -n gtodo2-%version

%build
export LDFLAGS="-lX11"

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

#TODO: check --disable-sm 
CC=/usr/sfw/bin/gcc CXX=/usr/sfw/bin/g++ ./configure --prefix=%{_prefix} \
            --disable-sm
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gtodo2
%{_datadir}/gtodo2/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Wed May 30 2007  - Thomas Wagner
- Initial spec
