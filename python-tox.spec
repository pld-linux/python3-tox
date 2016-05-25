# TODO:
# - packaging of 
#        /usr/bin/tox
#        /usr/bin/tox-quickstart


# Conditional build:
# %%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	tox
Summary:	Virtualenv-based automation of test activities
Summary(pl.UTF-8):	Oparta na Virtualenv automatyka testów
Name:		python-%{module}
Version:	2.3.1
Release:	2
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/46/39/e15a857fda1852da1485bc88ac4268dbcef037ab526e1ac21accf2a5c24c/tox-2.3.1.tar.gz
# Source0-md5:	9371b3d3e25c03751a0372e19602dfb9
URL:		http://tox.testrun.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-pluggy
BuildRequires:	python-virtualenv
BuildRequires:	python-pytest >= 2.3.5
BuildRequires:	python-pytest-timeout
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-pluggy
BuildRequires:	python3-virtualenv
BuildRequires:	python3-pytest >= 2.3.5
BuildRequires:	python3-pytest-timeout

%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tox is a generic virtualenv management and test command line tool you can use for:
- checking your package installs correctly with different Python versions and interpreters
- running your tests in each of the environments, configuring your test tool of choice
- acting as a frontend to Continuous Integration servers, greatly reducing boilerplate and merging CI and shell-based testing.

%description -l pl.UTF-8
Tox jest ogólnym, operatym na virtualenv narzędziem linii poleceń które może być użyte do:
- testowania czy pakiet instaluje się poprawnie z róznymi wersjami Pythona
- uruchamionia testów dla każdego ze środowisk, konfigurując narzędzia testowe
- jako frontend dla serwerów Continuous Integration, 

%package -n python3-%{module}
Summary:	Virtualenv-based automation of test activities
Summary(pl.UTF-8):	Oparta na Virtualenv automatyka testów
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Tox is a generic virtualenv management and test command line tool you can use for:
- checking your package installs correctly with different Python versions and interpreters
- running your tests in each of the environments, configuring your test tool of choice
- acting as a frontend to Continuous Integration servers, greatly reducing boilerplate and merging CI and shell-based testing.

%description -n python3-%{module} -l pl.UTF-8
Tox jest ogólnym, operatym na virtualenv narzędziem linii poleceń które może być użyte do:
- testowania czy pakiet instaluje się poprawnie z róznymi wersjami Pythona
- uruchamionia testów dla każdego ze środowisk, konfigurując narzędzia testowe
- jako frontend dla serwerów Continuous Integration, 

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG CONTRIBUTORS ISSUES.txt README.rst
%attr(755,root,root) %{_bindir}/tox
%attr(755,root,root) %{_bindir}/tox-quickstart
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG CONTRIBUTORS ISSUES.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
