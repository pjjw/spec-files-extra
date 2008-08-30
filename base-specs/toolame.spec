#
# spec file for package toolame.spec
#
# includes module(s): toolame
#

Name:                   toolame
Summary:                toolame  - optimized MPEG Audio Layer 2 encoder
Version:                02l
Source:                 %{sf_download}/toolame/toolame-%{version}.tgz
Patch1:			toolame-01-makefile.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %name-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

make -j$CPUS

%install
#make install DESTDIR=$RPM_BUILD_ROOT
[ ! -d $RPM_BUILD_ROOT%{_bindir} ] && mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 toolame $RPM_BUILD_ROOT%{_bindir}/toolame

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Aug 30 2008 - harry.lu@sun.com
- Use %sf_download instead of a specific server.
* Tue Mar 20 2007 - dougs@truemail.co.th
- Changed to be a base spec
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElame
- change to root:bin to follow other JDS pkgs.
- go back to 02l version of toolame because the beta tarball download site
  is gone.
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
