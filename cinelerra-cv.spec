# globals for cinelerra-cv-2.3-20150912gitc25d3b1.tar.bz2
%global gitdate 20150912
%global gitversion c25d3b1
%global gver .%{gitdate}git%{gitversion}
%global snapshot %{gitdate}git%{gitversion}

#ffmpeg 1.2.6 needs -D__STDC_CONSTANT_MACROS
%if 0%{?fedora} == 19
%global optflags %(echo %{optflags} -D__STDC_CONSTANT_MACROS )
%endif

#defaults switch _with_libmpeg3_system and global with_libmpeg3_system to 1
%{!?_with_libmpeg3_system: %{!?_without_libmpeg3_system: %global _with_libmpeg3_system 1}}
%{?_with_libmpeg3_system: %global with_libmpeg3_system 1}
%{?_without_libmpeg3_system: %global with_libmpeg3_system 0}

#defaults switch _with_ffmpeg_system and global with_ffmpeg_system to 1
%{!?_with_ffmpeg_system: %{!?_without_ffmpeg_system: %global _with_ffmpeg_system 1}}
%{?_with_ffmpeg_system: %global with_ffmpeg_system 1}
%{?_without_ffmpeg_system: %global with_ffmpeg_system 0}

Summary: Advanced audio and video capturing, compositing, and editing
Name: cinelerra-cv
Version: 2.3
Release: 1%{gver}%{?dist}
License: GPL
Group: Applications/Multimedia
URL: http://cinelerra-cv.org/
# cinelerra-cv-%{version}-%{snapshot}.tar.bz2 obtained with ./cinelerra-cv-snapshot.sh
Source0: cinelerra-cv-%{version}-%{snapshot}.tar.bz2
Source1: cinelerra-cv.conf
Source2: cinelerra-cv-snapshot.sh
Patch1: cinelerra-cv-desktop.patch
Patch2: cinelerra-cv-remove-fonts.patch
Patch5: cinelerra-cv-ffmpeg_api2.2.patch
Patch6: cinelerra-cv-ffmpeg2.0.patch

BuildRequires: autoconf, automake, libtool
BuildRequires: libXt-devel libXv-devel libXxf86vm-devel libXext-devel
BuildRequires: libXft-devel
BuildRequires: fontconfig-devel
BuildRequires: gettext-devel
Buildrequires: esound-devel
BuildRequires: alsa-lib-devel >= 1.0.2
BuildRequires: mjpegtools-devel
BuildRequires: libuuid-devel
# Required for libuuid
BuildRequires: e2fsprogs-devel
BuildRequires: fftw3-devel
BuildRequires: a52dec-devel
BuildRequires: lame-devel
BuildRequires: libsndfile-devel
BuildRequires: OpenEXR-devel
BuildRequires: faad2-devel
BuildRequires: libraw1394-devel >= 1.2.0
BuildRequires: libiec61883-devel
# >= 0.5.0 required because of the use of avc1394_vcr_get_timecode2
BuildRequires: libavc1394-devel >= 0.5.0
BuildRequires: x264-devel
BuildRequires: libogg-devel libvorbis-devel libtheora-devel
BuildRequires: libGL-devel libGLU-devel
# Stuff not checked by configure, but still required
BuildRequires: nasm
BuildRequires: freetype-devel
BuildRequires: faac-devel
BuildRequires: libjpeg-devel libpng-devel libtiff-devel
BuildRequires: imlib2-devel
BuildRequires: libdv-devel
Buildrequires: ffmpeg-devel
# Thiw is wip (should be used instead of toolame )
#BuildRequires: twolame-devel
%{?_with_libmpeg3_system:BuildRequires: libmpeg3-devel}
BuildRequires: desktop-file-utils

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
# Needed for the shmmax tweak
Requires(post): /sbin/sysctl
Requires(postun): /sbin/sysctl
# Needed fonts are provided once
Requires: bitstream-vera-fonts-common bitstream-vera-sans-fonts
Requires: bitstream-vera-sans-mono-fonts bitstream-vera-serif-fonts
Requires: mjpegtools
# if we use system libmpeg3
%{?_with_libmpeg3_system:Requires: libmpeg3-utils}

%description
Heroine Virtual Ltd. presents an advanced content creation system for Linux.

There are two types of moviegoers: producers who create new content, going back over their content at
future points for further refinement, and consumers who want to acquire the content and watch it.
Cinelerra is not intended for consumers.
Cinelerra has many features for uncompressed content, high resolution processing, and compositing,
with very few shortcuts.
Producers need these features because of the need to retouch many generations of footage with
alterations to the format, which makes Cinelerra very complex.

Cinelerra was meant to be a Broadcast 2000 replacement.

This is Community Version.

A professional audio and video editing software.


%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Provides:      cinelerra-devel
Obsoletes:     cinelerra-devel

%description devel
This is the Community maintained Version of cinelerra.

This package contains static libraries and header files need for development.

%prep
%setup -q
%patch1 -p1 -b .desktop
%patch2 -p1 -b .font_remove
%if %{with_ffmpeg_system}
%patch5 -p1 -b .ffmpeg_api
%patch6 -p1 -b .ffmpeg2.0
%endif

autoreconf -fi

%build

%configure \
  --with-buildinfo="Custom RPMFusion %{version}-%{release} version for Fedora/EPEL" \
  --program-suffix=-cv \
  --with-plugindir=%{_libdir}/%{name} \
%{?_with_libmpeg3_system: --with-external-libmpeg3 } \
%{?_with_ffmpeg_system: --with-external-ffmpeg } \
  --enable-opengl \
  --enable-freetype2 \
  --disable-static \
%ifarch %{ix86} x86_64
  --enable-mmx \
%else
  --disable-mmx \
  --disable-3dnow \
%endif
%ifarch ppc ppc64
  --enable-altivec \
%else
  --disable-altivec \
%endif
  --disable-rpath \
  FREETYPE_CFLAGS="-I%{_includedir}/freetype2" \

# remove executable stack
#export LDFLAGS+=" -Wl,-z,noexecstack"
#  --with-pic \
#  --with-fontsdir=%{_datadir}/fonts/%{name} \
#make

%{?_with_libmpeg3_system: rm -rf libmpeg3}

%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot} INSTALL="install -p"
%find_lang %{name}

# Install sysctl.d file
install -p -m 0644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysctl.d/cinelerra-cv.conf

desktop-file-install --vendor "" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --delete-original \
  --mode 644 \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# remove things not needed
find %{buildroot} -name '*.la' -exec rm -f {} ';'

#Fix execstack
#{_bindir}/execstack -c %{buildroot}%{_libdir}/%{name}/suv.so
#{_bindir}/execstack -c %{buildroot}%{_libdir}/%{name}/blondtheme.so
#{_bindir}/execstack -c %{buildroot}%{_libdir}/%{name}/bluedottheme.so
#{_bindir}/execstack -c %{buildroot}%{_bindir}/cinelerra-cv


%post
if [ $1 -eq 1 ]; then
  if [ $(/sbin/sysctl -n -q kernel.shmmax) -lt 2147483647 ] ; then
    # Hack for the package to work "out of the box".
    /sbin/sysctl -q -w kernel.shmmax=0x7fffffff
  fi
fi

/usr/bin/update-desktop-database &>/dev/null || :
/sbin/ldconfig

%postun
/usr/bin/update-desktop-database &>/dev/null || :
/sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING LICENSE
%{_bindir}/cinelerra-cv
%if %{with_libmpeg3_system} == 0
  %{_bindir}/mpeg3cat-cv
  %{_bindir}/mpeg3dump-cv
  %{_bindir}/mpeg3toc-cv
%endif
%{_bindir}/mplexlo-cv

%{_libdir}/*.so.*
%{_libdir}/%{name}
%if %{with_ffmpeg_system} == 0
%{_libdir}/vhook/drawtext.so
%{_libdir}/vhook/imlib2.so
%{_libdir}/vhook/fish.so
%{_libdir}/vhook/null.so
%{_libdir}/vhook/ppm.so
%{_libdir}/vhook/watermark.so
%endif
%{_datadir}/applications/cinelerra-cv.desktop
%{_datadir}/pixmaps/cinelerra-cv.xpm
%{_sysconfdir}/sysctl.d/cinelerra-cv.conf

%files devel
%doc ChangeLog NEWS README.BUILD TODO
%if %{with_libmpeg3_system} == 0
  %dir %{_includedir}/mpeg3
  %{_includedir}/mpeg3/*.h
  %{_libdir}/libmpeg3hv.so
%endif
%dir %{_includedir}/quicktime
%{_includedir}/quicktime/*.h
%{_libdir}/libguicast.so
%{_libdir}/libquicktimehv.so
%if %{with_ffmpeg_system} == 0
%{_libdir}/*cinelerra.so
%endif


%changelog
* Wed Dec 24 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.9.20141224git70b8c14
- Update to 20141224git70b8c14

* Sun Oct 12 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1.20141012git623e87e-1
- Update to git623e87e

* Sat Sep 27 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.8.20140927git9cbf7f0
- Update to cinelerra-cv-2.2.1-20140927git9cbf7f0

* Sun Jul 27 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.7.20140727git92dba16
- Update to 20140727 git 92dba16 .

* Sun May 25 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.5.20140525gitef4fddb
- Update to git ef4fddb
- Added cinelerra-cv-ffmpeg_api2.2.patch and cinelerra-cv-ffmpeg2.0.patch and build with external ffmpeg.
- make it work --with or --without libmpeg3_system and ffmpeg_system.

* Wed Apr 30 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.3.20140426git9154825
- Added imlib2-devel as BR to build vhook/imlib2.so

* Tue Apr 29 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.2.20140426git9154825
- Drop a file in /etc/sysctl.d instead to tweaking /etc/sysctl.conf
- Removed gcc-g++ as BR
- Use libmpeg3 from system
- Remove bundle fonts and fix font search path
- Scriptlet for desktop-database
- Disabled 3dnow
- Program-suffix -cv

* Mon Apr 28 2014 Sérgio Basto <sergio@serjux.com> - 2.2.1-0.1
- Initial spec, copied from David Vasquez and changed based on
  cinelerra-f15.spec from Atrpms and also changed based on
  openmamba/devel/specs/cinelerra-cv.spec

* Mon Sep 30 2013 David Vasquez <davidjeremias82@gmail.com> - 2.2-1
- Initial package creation for Fedora 19
- Spec inspirated in PKGBUILD Arch Linux
- Add freeing more shared memory from RPM Fusion