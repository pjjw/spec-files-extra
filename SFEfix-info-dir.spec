#
# spec file for package SFEfix-info-dir
#
# includes module(s): fix-info-dir
#
%include Solaris.inc

%define	src_name fix-info-dir
%define	src_url	http://ftp.pld-linux.org/software/fix-info-dir

Name:                SFEfix-info-dir
Summary:             Utility to fix infodir
Version:             0.13
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     fix-info-dir-01-gccism.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
cp fix-info-dir $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_sbindir}

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
