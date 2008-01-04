#
# spec file for package SFEputty
#
# use gcc to compile

%define CC gcc

%include Solaris.inc
Name:                    SFEputty
Summary:                 putty - A graphical SSH Client
URL:                     http://www.chiark.greenend.org.uk/~sgtatham/putty/
Version:                 0.60
Source:                  http://the.earth.li/~sgtatham/putty/latest/putty-%{version}.tar.gz
Patch1:			 putty-01-gtk.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc


%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n putty-%version
%patch1 -p1

%build

export CC=gcc
export CXX=g++
#be carefull *not* to set wired LDFLAGS in your compile-environment!
export LDFLAGS="${LDFLAGS} -lsocket -lxnet -L/usr/sfw/lib -R/usr/sfw/lib"
export INSTALL="/opt/jdsbld/bin/install -c -D"


cd unix

./configure --prefix=%{_prefix} \

make all-gtk all-cli

%install
bash
rm -rf $RPM_BUILD_ROOT
cd unix
#mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*


%changelog
* Fri Jan 04 2008 - Thomas Wagner
- add patch1 emailed by Takao.Fujiwara@Sun.COM (16 Nov 2007, putty-xx-my-build.diff)
* Fri July 20 2007  - Thomas Wagner
- Initial spec
