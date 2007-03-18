#
# spec file for package SFEmonodevelop
#
# includes module(s): monodevelop
#
%include Solaris.inc

Name:         SFEmonodevelop
Version:      0.13.1
Summary:      IDE for C# and other .NET languages
Source:       http://go-mono.com/sources/monodevelop/monodevelop-%{version}.tar.gz
URL:          http://monodevelop.org/
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEmono-devel
BuildRequires: SFEgtk-sharp
Requires: SUNWgnome-base-libs
Requires: SFEmono
Requires: SFEgtk-sharp
Requires: SFEgnome-sharp
Requires: SFEgtksourceview-sharp
Requires: SFEmonodoc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n monodevelop-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PATH=/usr/mono/bin:$PATH
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --without-gnome-screensaver \
            --disable-scrollkeeper \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

perl -pi -e 's/^#!\/bin\/sh/#!\/bin\/bash/' $RPM_BUILD_ROOT%{_bindir}/monodevelop
perl -pi -e 's/^#!\/bin\/sh/#!\/bin\/bash/' $RPM_BUILD_ROOT%{_bindir}/mdtool

#FIXME: need postrun script that runs update-mime-database
rm -r $RPM_BUILD_ROOT%{_datadir}/mime

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_libdir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/monodevelop
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_libdir}/locale
%endif

%changelog
* Sat Mar 17 2007 - laca@sun.com
- create!
