#
# spec file for package SFEfreedroid.spec
#
# includes module(s): freedroid
#
%include Solaris.inc

%define src_name	freedroidrpg
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/freedroid

Name:                   SFEfreedroidrpg
Summary:                FreeroidRPG Game
Version:                0.10.2
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1: 		freedroidrpg-01-wall.diff
Patch2: 		freedroidrpg-02-inline.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEfindutils
BuildRequires: SFEsdl-net-devel
Requires: SFEsdl-net
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export PATH=/usr/gnu/bin:$PATH
export CPPFLAGS="-D__FUNCTION__=__func__"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-fastmath		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/freedroidrpg
%{_mandir}

%changelog
* Fri Jul 13 2007 - dougs@truemail.co.th
- Bump to 0.10.2
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
