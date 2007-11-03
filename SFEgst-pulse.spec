#
# spec file for package SFEgst-pulse
#
# includes module(s): gst-pulse
#
%include Solaris.inc

%define gst_minmaj 0.10

Name:                    SFEgst-pulse
Summary:                 GNOME streaming media framework - PulseAudio plugin
URL:                     http://0pointer.de/lennart/projects/gst-pulse/
Version:                 0.9.5
Source:                  http://0pointer.de/lennart/projects/gst-pulse/gst-pulse-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SFEpulseaudio-devel
Requires:                SUNWgnome-media
Requires:                SFEpulseaudio

%include default-depend.inc

%prep
%setup -q -n gst-pulse-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gstreamer-%{gst_minmaj}/lib*.so*

%changelog
* Fri Nov 02 2007 - trisk@acm.jhu.edu
- Initial spec
