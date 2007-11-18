#
# spec file for package SFEscim-kmfl
#
# includes module(s): scim-kmfl
#
%include Solaris.inc

%define	src_name scim-kmfl-imengine
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/kmfl/scim-kmfl-imengine-0.9.5.tar.gz

Name:                SFEscim-kmfl
Summary:             SCIM kmfl imengine bridge
Version:             0.9.5
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     scim-kmfl-01-wall.diff
Patch2:		     scim-kmfl-02-strchr.diff
Patch3:		     scim-kmfl-03-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEscim-devel
Requires: SFEscim
BuildRequires: SFEkmflcomp-devel
Requires: SFEkmflcomp
BuildRequires: SFElibkmfl-devel
Requires: SFElibkmfl
Requires: SUNWxorg-headers

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/X11/include"
export CXXFLAGS="%cxx_optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal -I m4
automake -a -f
autoconf -f -I autoconf
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/doc $RPM_BUILD_ROOT%{_datadir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add SUNWxorg-headers dependency and set CXXFLAGS.
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
