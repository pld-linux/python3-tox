# TODO:
# - packaging of
#        /usr/bin/tox
#        /usr/bin/tox-quickstart
# - fix tests on builders

# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define		module	tox
Summary:	Virtualenv-based automation of test activities
Summary(pl.UTF-8):	Oparta na Virtualenv automatyka testów
Name:		python3-%{module}
Version:	4.24.2
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/t/tox/tox-%{version}.tar.gz
# Source0-md5:	a984de2e2b34da98ec42ce5d759290bf
URL:		http://tox.testrun.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-filelock
BuildRequires:	python3-flaky
BuildRequires:	python3-modules
BuildRequires:	python3-pluggy
BuildRequires:	python3-virtualenv
BuildRequires:	python3-pytest >= 2.3.5
BuildRequires:	python3-pytest-timeout
BuildRequires:	python3-py
Requires:	python3-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tox is a generic virtualenv management and test command line tool you
can use for:
- checking your package installs correctly with different Python
  versions and interpreters
- running your tests in each of the environments, configuring your
  test tool of choice
- acting as a frontend to Continuous Integration servers, greatly
  reducing boilerplate and merging CI and shell-based testing.

%description -l pl.UTF-8
Tox jest ogólnym, operatym na virtualenv narzędziem linii poleceń
które może być użyte do:
- testowania czy pakiet instaluje się poprawnie z róznymi wersjami
  Pythona
- uruchamionia testów dla każdego ze środowisk, konfigurując narzędzia
  testowe
- jako frontend dla serwerów Continuous Integration,

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/tox
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
