#
# spec file for package SFEgraveman
#
# includes module(s): graveman
#
%include Solaris.inc

%define SFEoggvorbis       %(/usr/bin/pkginfo -q SFEogg-vorbis && echo 1 || echo 0)

%define	src_name graveman
%define	src_url	 http://graveman.tuxfamily.org/sources

Name:                SFEgraveman
Summary:             A graphical front end to create or copy CDs and DVDs
Version:             0.3.12-5
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		         graveman-01-wall.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFElibid3tag
BuildRequires: SFElibid3tag-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
%if %SFEoggvorbis
Requires: SFEogg-vorbis
BuildRequires: SFEogg-vorbis-devel
%else
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
%endif
Requires: SUNWflac
BuildRequires: SUNWflac-devel
Requires: SFElibmng
BuildRequires: SFElibmng-devel
Requires: SUNWmkcd
Requires: SUNWdvdrw
Requires: SUNWzlib

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-D__sun__"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

autoreconf
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --mandir=%{_mandir}			\
            --datadir=%{_datadir}       \
            --enable-ogg                \
            --enable-flac               \
            --enable-mp3                \
            --enable-linux-ide          \
            --enable-linux-scsi

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/graveman
%{_mandir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%defattr (-, root, other)
%{_datadir}/locale

%changelog
* Thu Oct 11 2007 - ananth@sun.com
- Fixed attributes in the files section
* Sat Oct 06 2007 - ananth@sun.com
- Initial spec
