#
# Conditional build
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	cgit - a fast webinterface to git
Summary(pl.UTF-8):	cgit - szybki interfejs webowy do git-a
Name:		cgit
Version:	0.8.2
Release:	1
License:	GPL v2
Group:		Development/Tools
Source0:	http://hjemli.net/git/cgit/snapshot/%{name}-%{version}.tar.bz2
# Source0-md5:	872fafaa1ea6bd9292f312878864b665
Source1:	%{name}.conf
Source2:	%{name}-repo.conf
Source3:	%{name}-httpd.conf
Patch0:		%{name}-system-git.patch
Patch1:		%{name}-override-cflags.patch
URL:		http://hjemli.net/git/cgit
BuildRequires:	git-core-devel >= 1.6.1.1
BuildRequires:	openssl-devel
Requires:	webapps
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		webapp		cgit
%define		webappdir	%{_sysconfdir}/webapps/%{webapp}
%define		appdir		%{_datadir}/%{webapp}
%define		cgibindir	%{_prefix}/lib/cgi-bin

%description
Cgit is a CGI application implemented in C: it's basically (yet)
another git command, used to generate html. Cgit is not forking: all
git operations are performed by linking with libgit.a. It uses a
built-in cache: the generated html is stored on disk for the benefit
of later requests.

%description -l pl.UTF-8
Cgit to: napisana w C aplikacja CGI - zasadniczo jest to (kolejny)
interfejs do git-a, generujący kod html. Cgit jest aplikacją
nieforkującą - wszystkie operacje na repozytoriach wykonywane są z
użyciem biblioteki. Aplikacja ta korzysta z cache - wygenerowany kod
htl zapisany jest na dysku dla kolejnych żądań.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/git-core" \
	LDFLAGS="%{rpmldflags}" \
	LIBDIR=%{_libdir} \
	CGIT_CONFIG="%{webappdir}/%{webapp}.conf" \
	CGIT_SCRIPT_PATH="%{cgibindir}" \
	%{?with_verbose:V=1}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CGIT_CONFIG="%{webappdir}/%{webapp.conf}" \
	CGIT_SCRIPT_PATH="%{cgibindir}" \
	%{?with_verbose:V=1}

# css and logo
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{cgibindir}/%{name}.{css,png} $RPM_BUILD_ROOT%{appdir}

# cache
install -d $RPM_BUILD_ROOT/var/cache/cgit

# webapp stuff
install -d $RPM_BUILD_ROOT%{webappdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{webappdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{webappdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/apache.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{webapp}

%files
%defattr(644,root,root,755)
%doc README cgitrc.5.txt
%dir %{webappdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/cgit.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/cgit-repo.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{webappdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,root) %{webappdir}/httpd.conf
%attr(755,root,root) %{cgibindir}/cgit.cgi
%attr(770,root,http) /var/cache/cgit
%{appdir}
